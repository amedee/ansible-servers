#!/usr/bin/env python3
"""
sendgrid_sendmail.py

A script to send emails using SendGrid API.
Reads an email from stdin and forwards it via SendGrid, preserving attachments.
"""

import email
import logging
import sys
import traceback

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
)

# Setup logging
LOG_FILE = "/var/log/sendgrid-sendmail.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

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
                attachment = Attachment()
                attachment.file_content = FileContent(
                    part.get_payload(decode=True).decode("utf-8", errors="ignore")
                )
                attachment.file_type = FileType(part.get_content_type())
                attachment.file_name = FileName(part.get_filename())
                attachment.disposition = Disposition("attachment")
                attachments.append(attachment)
            except (UnicodeDecodeError, AttributeError) as exc:
                # UnicodeDecodeError for decode issues,
                # AttributeError if part.get_filename() is None or similar
                logging.warning("Failed to process attachment: %s", exc)
    return attachments


def extract_body(msg):
    """
    Extract plain text and HTML body parts from an email message.

    Returns:
        tuple: (plain_text, html_text)
    """
    plain = None
    html = None
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = part.get("Content-Disposition", "")
            if "attachment" in disposition:
                continue
            charset = part.get_content_charset() or "utf-8"
            try:
                content = part.get_payload(decode=True).decode(
                    charset, errors="replace"
                )
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
            content = msg.get_payload(decode=True).decode(charset, errors="replace")
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
        except (email.errors.MessageError, UnicodeDecodeError) as exc:
            logging.error("Failed to parse email message: %s", exc)
            sys.exit(1)

        from_email = msg["From"]
        to_emails = msg.get_all("To", [])
        cc_emails = msg.get_all("Cc", [])
        bcc_emails = msg.get_all("Bcc", [])
        all_recipients = to_emails + cc_emails + bcc_emails

        # Remove Bcc to avoid leaking
        if "Bcc" in msg:
            del msg["Bcc"]

        plain_body, html_body = extract_body(msg)
        attachments = extract_attachments(msg)

        sendgrid_client = SendGridAPIClient(read_api_key())
        email_msg = Mail(
            from_email=Email(from_email),
            to_emails=all_recipients,
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
                "Email sent: From=%s, To=%s", from_email, ",".join(all_recipients)
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
