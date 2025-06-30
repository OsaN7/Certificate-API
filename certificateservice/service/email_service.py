"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 15/05/2025
"""
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown

from certificateservice.domain.email import EmailDetail
from certificateservice.settings import Settings
from certificateservice.utils import loggerutil

import asyncio


class EmailService:
    def __init__(self, smtp_server: str = None, smtp_port: int = 0, sender_email: str = None,
                 sender_password: str = None):
        self.logger = loggerutil.get_logger(__name__)
        self.smtp_host = smtp_server or Settings.SMTP_HOST
        self.smtp_port = smtp_port if smtp_port > 0 else Settings.SMTP_PORT
        self.sender_email = sender_email or Settings.SENDER_EMAIL
        self.sender_password = sender_password or Settings.SENDER_PASSWORD
        self.default_recipients = Settings.RECIPIENT_EMAILS  # Comma separated string
        self.server = None
        self.enabled = Settings.ENABLE_EMAIL_SERVICE
        if self.enabled:
            self.connect()

    def connect(self, ):
        try:
            if self.smtp_host is None or self.smtp_port <= 0 or self.sender_email is None or self.sender_password is None:
                self.logger.warning("Email SMTP configuration is not set.")
                return
            self.server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            self.server.starttls()
            self._login()
        except Exception as e:
            self.logger.exception(f"Failed to connect to SMTP server: {e}")

    def _login(self):
        try:
            if self.server is None:
                self.logger.warning("SMTP server is not connected.")
                return
            self.server.login(self.sender_email, self.sender_password)
            self.logger.debug("Connected to SMTP server")
        except Exception as e:
            self.logger.exception(f"Failed to login to SMTP server: {e}")

    def send(self, recipient_emails: str, subject: str, message: str, attachments: list[str] = None,
             message_type: str = 'plain') -> bool:
        if not self.enabled:
            self.logger.warning("Email alerts are disabled.")
            return False
        try:
            res = self.server.noop()
            if res[0] != 250:
                self.logger.warning("SMTP server is not responding.")
                self.connect()
            self._send(recipient_emails=recipient_emails, subject=subject, message=message, attachments=attachments,
                       message_type=message_type)
            return True
        except Exception as e:
            self.logger.exception(f"Failed to send email: {e}")
            return False

    def _send(self, recipient_emails: str, subject, message, attachments: list[str] = None,
              message_type: str = 'plain'):
        """
        :param recipient_emails:  Comma separated string of recipient emails
        :param subject:  Email subject
        :param message: Email message content
        :param attachments:  List of file paths to attach to the email
        :param message_type: plain, html, or markdown
        :return:
        """
        if recipient_emails is None:
            recipients = self.default_recipients
        else:
            recipients = recipient_emails
        message_type = message_type if message_type in ['text', 'html', 'markdown'] else 'plain'

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipients
        msg['Subject'] = subject

        if message_type == "markdown":
            message = markdown.markdown(message)
            message_type = "html"

        msg.attach(MIMEText(message, message_type))

        if attachments:
            for attachment_path in attachments:
                if attachment_path and os.path.isfile(attachment_path):
                    with open(attachment_path, "rb") as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition',
                                        f'attachment; filename={os.path.basename(attachment_path)}')
                        msg.attach(part)

        self.server.send_message(msg)
        self.logger.debug(f"Email sent to {recipients}")

    def send_email(self, email: EmailDetail) -> bool:
        try:
            return self.send(
                recipient_emails=email.recipient_email,
                subject=email.subject,
                message=email.message,
                attachments=email.attachments,
                message_type=email.message_type
            )
        except Exception as e:
            self.logger.exception(f"Failed to send email: {e}")
            return False

    def send_in_batch(self, emails: list[tuple[int, EmailDetail]]) -> list[tuple[int, bool]]:
        results: list[tuple[int, bool]] = []
        try:
            for index, email in emails:
                status = self.send_email(email=email)
                results.append((index, status))
                msg = "Sent" if status else "Failed"
                print(f"Email:[{msg}]-{index}-{email.recipient_email}, subject: {email.subject}")
            return results
        except Exception as e:
            self.logger.exception(f"Failed to send batch emails: {e}")
            return results
