"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 27/06/2025
"""
import asyncio
import os
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown
from aiosmtplib import SMTP

from certificateservice.domain.email import EmailDetail
from certificateservice.settings import Settings
from certificateservice.utils import loggerutil


class EmailServiceAsync:
    def __init__(self, smtp_server: str = None, smtp_port: int = 0, sender_email: str = None,
                 sender_password: str = None, parallel_count=10, pool_size=5):
        self.logger = loggerutil.get_logger(__name__)
        self.smtp_host = smtp_server or Settings.SMTP_HOST
        self.smtp_port = smtp_port if smtp_port > 0 else Settings.SMTP_PORT
        self.sender_email = sender_email or Settings.SENDER_EMAIL
        self.sender_password = sender_password or Settings.SENDER_PASSWORD
        self.default_recipients = Settings.RECIPIENT_EMAILS
        self.enabled = Settings.ENABLE_EMAIL_SERVICE
        self.semaphore = asyncio.Semaphore(parallel_count)
        self.pool_size = pool_size
        self.smtp_pool = asyncio.Queue()

    async def connect(self):
        try:
            print("Connecting to SMTP server...")
            for _ in range(self.pool_size):
                if self.smtp_host is None or self.smtp_port <= 0 or self.sender_email is None or self.sender_password is None:
                    self.logger.warning("Email SMTP configuration is not set.")
                    return
                smtp = SMTP(hostname=self.smtp_host, port=self.smtp_port, start_tls=True)
                await smtp.connect()
                await smtp.login(self.sender_email, self.sender_password)
                await self.smtp_pool.put(smtp)
        except Exception as e:
            self.logger.exception(f"Failed to connect to SMTP server: {e}")

    async def send(self, recipient_emails: str, subject, message, attachments: list[str] = None,
                   message_type: str = 'plain') -> bool:
        smtp = None
        try:
            if not self.enabled:
                self.logger.warning("Email alerts are disabled.")
                return False
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

            smtp = await self.smtp_pool.get()
            if smtp is None:
                self.logger.error("No SMTP connection available in the pool.")
                await self.connect()
                smtp = await self.smtp_pool.get()
            await smtp.send_message(msg)
            self.logger.debug(f"Email sent to {recipients}")
        except Exception as e:
            self.logger.exception(f"Failed to send the email: {e}")
            return False
        finally:
            if smtp:
                await self.smtp_pool.put(smtp)
        return True

    async def send_in_batch(self, emails: list[tuple[int, EmailDetail]]) -> list[tuple[int, bool]]:
        """
        :param emails:  [(index, EmailDetail), ...]
        :return:
        """
        print(f"Got {len(emails)} emails to send")

        async def _send_with_semaphore(index, email: EmailDetail):
            async with self.semaphore:
                start_time = time.time()

                status = await self.send(
                    recipient_emails=email.recipient_email,
                    subject=email.subject,
                    message=email.message,
                    attachments=email.attachments,
                    message_type=email.message_type)
                # self.logger.debug(f"Email: {index} - [{"sent" if status else "not sent"}] to {email.recipient_email}")
                print(
                    f"Email: {index} - [{"sent" if status else "not sent"}] to {email.recipient_email}, Time: {time.time() - start_time:.2f} seconds")
                return index, status

        tasks = [
            _send_with_semaphore(index=index, email=email) for index, email in emails
        ]
        results = await asyncio.gather(*tasks)
        return results
