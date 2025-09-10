#!/usr/bin/env python3
import sys
import os
import logging
import logging.handlers
import boto3
from email import message_from_binary_file

# Setup syslog logging
logger = logging.getLogger("ses_sendmail")
logger.setLevel(logging.INFO)
syslog = logging.handlers.SysLogHandler(address='/dev/log')
formatter = logging.Formatter('ses_sendmail: %(levelname)s %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

def main():
    # Read raw email from stdin
    try:
        msg = message_from_binary_file(sys.stdin.buffer)
    except Exception as e:
        logger.error(f"Failed to read email from stdin: {e}")
        sys.exit(1)

    # Extract recipients from headers
    recipients = []
    for header in ("To", "Cc", "Bcc"):
        if header in msg:
            for addr in msg[header].split(','):
                addr = addr.strip()
                if addr:
                    recipients.append(addr)

    if not recipients:
        logger.error("No valid recipients found")
        sys.exit(1)

    # Send via SES
    try:
        ses = boto3.client("ses", region_name="eu-central-1",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
        response = ses.send_raw_email(
            Source=msg.get("From"),
            Destinations=recipients,
            RawMessage={"Data": msg.as_bytes()}
        )
        logger.info(f"Email sent successfully to: {', '.join(recipients)}; SES MessageId: {response['MessageId']}")
    except Exception as e:
        logger.error(f"Failed to send email via SES: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
