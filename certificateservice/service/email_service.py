"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 15/05/2025
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from certificateservice.utils import loggerutil


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
        self.enabled = Settings.ENABLE_EMAIL_ALERT
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

    def send(self, subject, message, recipient_email: str = None):
        if not self.enabled:
            self.logger.warning("Email alerts are disabled.")
            return
        try:
            res = self.server.noop()
            if res[0] != 250:
                self.logger.warning("SMTP server is not responding.")
                self.connect()
            self._send(subject, message, recipient_email)
        except Exception as e:
            self.logger.exception(f"Failed to send email: {e}")

    def _send(self, subject, message, recipient_email: str = None):
        if recipient_email is None:
            recipients = self.default_recipients
        else:
            recipients = recipient_email
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipients
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        self.server.send_message(msg)
        self.logger.debug(f"Email sent to {recipients}")
