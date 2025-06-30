"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 15/06/2025
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_PORT = int(os.getenv("API_PORT", 8000))
    OUTPUT_BASE_DIR = "data/certificates"

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    SMTP_HOST: str = os.getenv("SMTP_HOST", None)
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 0))
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", None)
    SENDER_PASSWORD: str = os.getenv("SENDER_PASSWORD", None)
    RECIPIENT_EMAILS: str = os.getenv("RECIPIENT_EMAILS", None)
    ENABLE_EMAIL_SERVICE: bool = os.getenv("ENABLE_EMAIL_SERVICE", "False").lower() == "true"

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:osan@localhost:5432/certificate").strip()
