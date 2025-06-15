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
from email.errors import MessageError
from email.utils import getaddresses, parseaddr

from requests.exceptions import RequestException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Disposition,
    Email,
    FileContent,
    FileName,
    FileType,
    Mail,
    To,
)

# Send logging messages to syslog under "local0"
handler = logging.handlers.SysLogHandler(address="/dev/log", facility="local0")
formatter = logging.Formatter(
    "sendgrid_sendmail[ %(process)d ] %(levelname)s: %(message)s"
)
handler.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(logging.INFO)
root.handlers = [handler]

API_KEY_PATH = "/etc/sendgrid/api_key"


def read_api_key():
    """Read SendGrid API key from a file."""
    try:
        with open(API_KEY_PATH, "r", encoding="utf-8") as file_handle:
            return file_handle.read().strip()
    except OSError:
        logging.error("Failed to read SendGrid API key from configured path.")
        sys.exit(1)


def extract_attachments(msg):
    """Extract attachments from an email message and convert to SendGrid Attachment objects."""
    attachments = []
    for part in msg.walk():
        if part.is_multipart():
            continue
        content_disposition = part.get("Content-Disposition", "")
        if "attachment" in content_disposition:
            try:
                payload = part.get_payload(decode=True)
                if payload is None:
                    logging.warning(
                        "Attachment payload is None for filename %s",
                        part.get_filename(),
                    )
                    continue
                attachment = Attachment()
                # SendGrid expects base64 encoded content as a string
                encoded_content = base64.b64encode(payload).decode("ascii")
                attachment.file_content = FileContent(encoded_content)
                attachment.file_type = FileType(part.get_content_type())
                attachment.file_name = FileName(part.get_filename() or "attachment")
                attachment.disposition = Disposition("attachment")
                attachments.append(attachment)
            except (UnicodeDecodeError, AttributeError) as exc:
                logging.warning("Failed to process attachment: %s", exc)
    return attachments


def extract_body(msg):
    """
    Extract plain text and HTML body parts from an email message.

    Returns:
        (plain, html)
    """
    plain = None
    html = None
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = part.get("Content-Disposition", "")
            if "attachment" in disposition.lower():
                continue
            charset = part.get_content_charset() or "utf-8"
            try:
                payload = part.get_payload(decode=True)
                if payload is None:
                    logging.debug("Ignoring empty body part.")
                    continue
                content = payload.decode(charset, errors="replace")
                if content_type == "text/plain" and plain is None:
                    plain = content
                elif content_type == "text/html" and html is None:
                    html = content
            except (UnicodeDecodeError, AttributeError) as exc:
                logging.warning("Failed to decode part: %s", exc)
    else:
        content_type = msg.get_content_type()
        charset = msg.get_content_charset() or "utf-8"
        try:
            payload = msg.get_payload(decode=True)
            if payload is None:
                logging.warning("Singlepart message payload is None")
            else:
                content = payload.decode(charset, errors="replace")
                if content_type == "text/plain":
                    plain = content
                elif content_type == "text/html":
                    html = content
        except (UnicodeDecodeError, AttributeError) as exc:
            logging.warning("Failed to decode singlepart message: %s", exc)
    return plain, html


def main():
    """Main function: read email from stdin and send it via SendGrid."""
    try:
        raw_email = sys.stdin.read()
        try:
            msg = email.message_from_string(raw_email)
        except (MessageError, UnicodeDecodeError) as exc:
            logging.error("Failed to parse email message: %s", exc)
            sys.exit(1)

        from_email_raw = msg["From"]
        _, from_email_addr = parseaddr(from_email_raw or "")
        if not from_email_addr:
            logging.error("Invalid or missing From address")
            sys.exit(1)

        # Collect all recipients from To, Cc, Bcc headers
        recipient_headers = []
        for header in ["To", "Cc", "Bcc"]:
            recipient_headers.extend(msg.get_all(header, []))
        addresses = getaddresses(recipient_headers)
        to_emails = [To(addr) for _, addr in addresses if addr]

        if not to_emails:
            logging.error("No valid recipients found in To, Cc, or Bcc")
            sys.exit(1)

        # Remove Bcc header to avoid leaking Bcc addresses
        if "Bcc" in msg:
            del msg["Bcc"]

        plain_body, html_body = extract_body(msg)
        attachments = extract_attachments(msg)

        sendgrid_client = SendGridAPIClient(read_api_key())
        email_msg = Mail(
            from_email=Email(from_email_addr),
            to_emails=to_emails,
            subject=msg["Subject"] or "(No Subject)",
            plain_text_content=plain_body or " ",
            html_content=html_body,
        )

        for att in attachments:
            email_msg.add_attachment(att)

        try:
            response = sendgrid_client.send(email_msg)
        except RequestException as exc:
            logging.error("SendGrid request error: %s", exc)
            sys.exit(1)
        except Exception:  # pylint: disable=all
            logging.error("Unexpected error sending email:\n%s", traceback.format_exc())
            sys.exit(1)

        if 200 <= response.status_code < 300:
            logging.info(
                "Email sent: From=%s, To=%s",
                from_email_addr,
                ",".join([e.email for e in to_emails]),
            )
            sys.exit(0)
        else:
            logging.error("SendGrid error %d: %s", response.status_code, response.body)
            sys.exit(1)

    except Exception:  # pylint: disable=all
        logging.error("Unexpected error:\n%s", traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
