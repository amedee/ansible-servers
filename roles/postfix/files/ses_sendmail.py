#!/usr/bin/env python3
"""
SES sendmail wrapper.

Reads a raw email from stdin and submits it to Amazon SES using the
`send_raw_email` API call. Designed to be called by Postfix as a transport.
Logs to syslog and exits with a non-zero code on failure.
"""

import logging
import logging.handlers
import os
import sys
from email import message_from_binary_file
from email.message import Message
from typing import List

import boto3
from botocore.exceptions import BotoCoreError, ClientError

__version__ = "1.0.0"

# Configuration (pulled once at import time)
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-central-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Setup syslog logging
logger = logging.getLogger("ses_sendmail")
logger.setLevel(logging.INFO)
syslog = logging.handlers.SysLogHandler(address="/dev/log")
formatter = logging.Formatter("ses_sendmail: %(levelname)s %(message)s")
syslog.setFormatter(formatter)
logger.addHandler(syslog)


def extract_recipients(msg: Message) -> List[str]:
    """Extract recipients from To, Cc, and Bcc headers."""
    recipients: List[str] = []
    for header in ("To", "Cc", "Bcc"):
        if header in msg:
            for addr in msg[header].split(","):
                addr = addr.strip()
                if addr:
                    recipients.append(addr)
    return recipients


def send_via_ses(msg: Message, recipients: List[str]) -> str:
    """
    Send a raw email message via Amazon SES.

    :param msg: Email Message object.
    :param recipients: List of recipients.
    :return: SES MessageId on success.
    """
    ses = boto3.client(
        "ses",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = ses.send_raw_email(
        Source=msg.get("From"),
        Destinations=recipients,
        RawMessage={"Data": msg.as_bytes()},
    )
    return response["MessageId"]


def main() -> None:
    """Read email from stdin, extract recipients, and send via SES."""
    try:
        msg = message_from_binary_file(sys.stdin.buffer)
    except (OSError, ValueError) as exc:
        logger.error("Failed to read email from stdin: %s", exc)
        sys.exit(1)

    recipients = extract_recipients(msg)
    if not recipients:
        logger.error("No valid recipients found")
        sys.exit(1)

    try:
        message_id = send_via_ses(msg, recipients)
        logger.info(
            "Email sent successfully to: %s; SES MessageId: %s",
            ", ".join(recipients),
            message_id,
        )
    except (BotoCoreError, ClientError) as exc:
        logger.error("Failed to send email via SES: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(
            "Usage: ses_sendmail.py < message.eml\n"
            "Reads a raw email from stdin and sends it via Amazon SES.\n"
            "Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION."
        )
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] in ("-v", "--version"):
        print(f"ses_sendmail.py version {__version__}")
        sys.exit(0)

    main()
