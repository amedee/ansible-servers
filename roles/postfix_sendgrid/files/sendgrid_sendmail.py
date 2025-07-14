#!/usr/bin/env python3
"""
sendgrid_sendmail.py

A script to send emails using SendGrid API.
Reads an email from stdin and forwards it via SendGrid, preserving attachments.

Logging is routed to syslog instead of a file.
"""
import base64
import email
import logging
import logging.handlers
import sys
import traceback
from dataclasses import dataclass
from email.errors import MessageError
from email.utils import getaddresses, parseaddr
from typing import List, Optional

import requests.exceptions
from email_validator import EmailNotValidError, validate_email
from python_http_client.exceptions import HTTPError
from requests.exceptions import RequestException, Timeout
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Disposition,
    Email,
    FileContent,
    FileName,
    FileType,
    Header,
    Mail,
    To,
)
from sendgrid.helpers.mail.exceptions import SendGridException

EX_OK = 0
EX_SOFTWARE = 1
EX_TEMPFAIL = 75
HTTP_SUCCESS_MIN = 200
HTTP_SUCCESS_MAX = 300

API_KEY_PATH = "/etc/sendgrid/api_key"


@dataclass
class _EmailContent:
    from_email: str
    to_emails: list
    subject: Optional[str]
    plain_body: str
    html_body: Optional[str]
    attachments: List


# Send logging messages to syslog under "local0"
syslog_handler = logging.handlers.SysLogHandler(address="/dev/log", facility="local0")
syslog_formatter = logging.Formatter(
    "sendgrid_sendmail[ %(process)d ] %(levelname)s: %(message)s"
)
syslog_handler.setFormatter(syslog_formatter)

# Also log to a file for debugging
file_handler = logging.FileHandler("/var/log/sendgrid_sendmail/debug.log")
file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(file_formatter)

# Combine both handlers
root = logging.getLogger()
root.setLevel(logging.INFO)
root.handlers = [syslog_handler, file_handler]


def _read_api_key():
    """Read SendGrid API key from a file."""
    try:
        with open(API_KEY_PATH, "r", encoding="utf-8") as file_handle:
            return file_handle.read().strip()
    except OSError:
        logging.error("Failed to read SendGrid API key from configured path.")
        sys.exit(EX_SOFTWARE)


def _extract_attachments(msg):
    """Extract attachments from an email message and convert to SendGrid Attachment objects."""
    attachments = []
    for part in msg.walk():
        if part.is_multipart():
            continue
        if "attachment" in (part.get("Content-Disposition") or ""):
            attachment = _build_sendgrid_attachment(part)
            if attachment:
                attachments.append(attachment)
    return attachments


def _build_sendgrid_attachment(part):
    """Convert a MIME part to a SendGrid Attachment, or return None if invalid."""
    try:
        payload = part.get_payload(decode=True)
        if payload is None:
            logging.warning(
                "Attachment payload is None for filename %s", part.get_filename()
            )
            return None
        encoded_content = base64.b64encode(payload).decode("ascii")
        attachment = Attachment()
        attachment.file_content = FileContent(encoded_content)
        attachment.file_type = FileType(part.get_content_type())
        attachment.file_name = FileName(part.get_filename() or "attachment")
        attachment.disposition = Disposition("attachment")
        return attachment
    except (UnicodeDecodeError, AttributeError) as exc:
        logging.warning("Failed to process attachment: %s", exc)
        return None


def _extract_body(msg):
    """
    Extract plain text and HTML body parts from an email message.

    Returns:
        (plain, html)
    """
    if msg.is_multipart():
        return _extract_body_from_multipart(msg)
    return _extract_body_from_singlepart(msg)


def _extract_body_from_multipart(msg):
    plain = None
    html = None
    for part in msg.walk():
        if _is_attachment(part):
            continue
        content_type = part.get_content_type()
        content = _safe_decode_payload(part)
        if content is None:
            continue
        if content_type == "text/plain" and plain is None:
            plain = content
        elif content_type == "text/html" and html is None:
            html = content
    return plain, html


def _extract_body_from_singlepart(msg):
    plain = None
    html = None
    content = _safe_decode_payload(msg)
    if content:
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            plain = content
        elif content_type == "text/html":
            html = content
    return plain, html


def _is_attachment(part):
    disposition = part.get("Content-Disposition", "")
    return "attachment" in disposition.lower()


def _safe_decode_payload(part):
    charset = part.get_content_charset() or "utf-8"
    try:
        payload = part.get_payload(decode=True)
        if payload is None:
            logging.debug("Empty payload")
            return None
        return payload.decode(charset, errors="replace")
    except (UnicodeDecodeError, AttributeError) as exc:
        logging.warning("Failed to decode part: %s", exc)
        return None


def _is_valid_email(address):
    """
    Validate email address
    """
    try:
        validate_email(address, allow_smtputf8=True)
        return True
    except EmailNotValidError as exc:
        logging.warning("Invalid email address %s: %s", address, exc)
        return False


def _normalize_recipients(addresses):
    """
    Validate and normalize a list of recipient email addresses.

    Args:
        addresses (list of tuples): [(name, email), ...]

    Returns:
        list of sendgrid.helpers.mail.To objects
    """
    to_emails = []
    invalid = []

    for name, email_addr in addresses:
        try:
            validated = validate_email(email_addr, allow_smtputf8=True)
            normalized_email = validated.email
            to_emails.append(To(email=normalized_email, name=name))
        except EmailNotValidError as exc:
            logging.warning("Invalid recipient address %s: %s", email_addr, exc)
            invalid.append(email_addr)

    if invalid:
        logging.error("Invalid recipient addresses: %s", ", ".join(invalid))
        sys.exit(EX_SOFTWARE)

    return to_emails


def _extract_custom_headers(msg):
    """
    Return a dict of custom headers that should be passed along.
    Excludes standard headers handled by the SendGrid Mail object.
    """
    skip_headers = {
        "bcc",
        "cc",
        "content-transfer-encoding",
        "content-type",
        "date",
        "dkim-signature",
        "from",
        "message-id",
        "mime-version",
        "received",
        "reply-to",
        "return-path",
        "subject",
        "to",
    }

    custom_headers = {}
    for key, value in msg.items():
        if key.lower() not in skip_headers:
            custom_headers[key] = value
    return custom_headers


def _parse_raw_email(raw_email):
    try:
        return email.message_from_string(raw_email)
    except (MessageError, UnicodeDecodeError) as exc:
        logging.error("Failed to parse email message: %s", exc)
        sys.exit(EX_SOFTWARE)


def _extract_and_validate_sender(msg):
    from_email_raw = msg["From"]
    _, from_email_addr = parseaddr(from_email_raw or "")

    try:
        validated = validate_email(from_email_addr, allow_smtputf8=True)
        return validated.email
    except EmailNotValidError as exc:
        logging.error("Invalid From address: %s (%s)", from_email_addr, exc)
        sys.exit(EX_SOFTWARE)


def _extract_and_validate_recipients(msg):
    recipient_headers = []
    for header in ["To", "Cc", "Bcc"]:
        recipient_headers.extend(msg.get_all(header, []))

    addresses = getaddresses(recipient_headers)
    to_emails = _normalize_recipients(addresses)

    if not to_emails:
        logging.error("No valid recipients found in To, Cc, or Bcc")
        sys.exit(EX_SOFTWARE)

    invalid = [to.email for to in to_emails if not _is_valid_email(to.email)]
    if invalid:
        logging.error("Invalid recipient addresses: %s", ", ".join(invalid))
        sys.exit(EX_SOFTWARE)

    return to_emails


def _remove_bcc_header(msg):
    if "Bcc" in msg:
        del msg["Bcc"]


def _build_sendgrid_mail(content: _EmailContent):
    email_msg = Mail(
        from_email=Email(content.from_email),
        to_emails=content.to_emails,
        subject=content.subject or "(No Subject)",
        plain_text_content=content.plain_body or " ",
        html_content=content.html_body,
    )
    for att in content.attachments:
        email_msg.add_attachment(att)
    return email_msg


def _add_custom_headers(msg, email_msg):
    headers = _extract_custom_headers(msg)
    if headers:
        clean = {str(k): " ".join(str(v).splitlines()) for k, v in headers.items()}
        for p in email_msg.personalizations:
            for k, v in clean.items():
                p.add_header(Header(k, v))


def _send_email_via_sendgrid(email_msg, from_email, to_emails, subject):
    try:
        client = SendGridAPIClient(_read_api_key())
        response = client.send(email_msg)
    except RequestException as exc:
        logging.error("SendGrid request error: %s", exc)
        sys.exit(EX_TEMPFAIL)
    except (
        HTTPError,
        SendGridException,
        Timeout,
        requests.exceptions.ConnectionError,
    ) as exc:
        logging.error("SendGrid transport error: %s", exc)
        sys.exit(EX_TEMPFAIL)
    except Exception:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error sending email:\n%s", traceback.format_exc())
        sys.exit(EX_TEMPFAIL)

    if HTTP_SUCCESS_MIN <= response.status_code < HTTP_SUCCESS_MAX:
        logging.info(
            "Email sent: From=%s, To=%s, Subject=%s",
            from_email,
            ",".join([e.email for e in to_emails]),
            subject or "(No Subject)",
        )
        sys.exit(EX_OK)
    else:
        logging.error("SendGrid error %d: %s", response.status_code, response.body)
        sys.exit(EX_SOFTWARE)


def main():
    """Main function: read email from stdin and send it via SendGrid."""
    try:
        raw_email = sys.stdin.read()
        msg = _parse_raw_email(raw_email)
        from_email_addr = _extract_and_validate_sender(msg)
        to_emails = _extract_and_validate_recipients(msg)
        _remove_bcc_header(msg)

        plain_body, html_body = _extract_body(msg)
        attachments = _extract_attachments(msg)
        content = _EmailContent(
            from_email=from_email_addr,
            to_emails=to_emails,
            subject=msg["Subject"],
            plain_body=plain_body,
            html_body=html_body,
            attachments=attachments,
        )
        email_msg = _build_sendgrid_mail(content)

        _add_custom_headers(msg, email_msg)

        _send_email_via_sendgrid(email_msg, from_email_addr, to_emails, msg["Subject"])
    except Exception:  # pylint: disable=broad-exception-caught
        logging.error("Unexpected error:\n%s", traceback.format_exc())
        sys.exit(EX_SOFTWARE)


if __name__ == "__main__":
    main()
