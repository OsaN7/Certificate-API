"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 17/06/2025
"""
import asyncio
from textwrap import dedent

import pandas as pd

from certificateservice.domain.email import EmailDetail
from certificateservice.service.email_service import EmailService
from certificateservice.service.email_service_async import EmailServiceAsync


def create_message(template: str, placeholders: dict) -> str:
    """
    Generate a message from a template and placeholders.
    """
    if not template:
        return ""
    if not placeholders:
        return template
    return template.format(**placeholders)


PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE = """
        Dear {name},

        Thank you for participating in the **{event}**.  
        We truly appreciate your involvement and enthusiasm.

        Please find your certificate of participation attached.

        Best regards,  
        **Pascal College, Lalitpur, Nepal**  
        *A College Run by IT Professionals*  
        Phone: +977 15916910  
        Website: [www.pascalcollege.edu.np](https://www.pascalcollege.edu.np/)  

        **Connect with us:**  
        [Facebook](https://www.facebook.com/pascal.national.college) | [YouTube](https://www.youtube.com/@pascal.national.college) | [X (Twitter)](https://x.com/pascal_college)  
        [LinkedIn](https://www.linkedin.com/company/pascalcollege) | [Instagram](https://www.instagram.com/pascal.college/) | [TikTok](https://www.tiktok.com/@pascalcollege)
    """


def send_email_example():
    email_service = EmailService()
    subject = "Certificate of Participation for Webinar on B.Sc. CSIT Internship Report Writing"
    message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()

    placeholders = {
        "name": "Nishma Gautam",
        "event": "Webinar on CSIT Internship Report Writing"
    }
    message = create_message(message_template, placeholders)
    email = EmailDetail(
        recipient_email="asokpant@gmail.com",
        subject=subject,
        message=message,
        message_type="markdown",
        attachments=[
            "data/certificates/20250510-webinar-csit-internship-report/20250510-webinar-080bca13.nishma@scst.edu.np-Nishma Gautam.pdf"]
    )
    success = email_service.send_email(email=email)
    print(f"Email {"sent" if success else "not sent"} to {email.recipient_email} with subject: {email.subject}")


def send_csit_internship_report_writing_certificate(email_service: EmailService):
    event_name = "National Webinar on B.Sc. CSIT Internship Report Writing"
    subject = f"Certificate of Participation - {event_name}"
    message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()
    certificates_csv = "data/certificates/20250510-webinar-csit-internship-report/certificates.csv"
    df = pd.read_csv(certificates_csv)

    for index, row in df.iterrows():
        is_email_sent = row.get("email_sent", False)
        is_email_sent = False if pd.isna(is_email_sent) else bool(is_email_sent)

        if is_email_sent:
            print(f"Email already sent for {index}: {row.get('name', 'Participant')}. Skipping...")
            continue
        name = row.get("name", "Participant")
        recipient_email = "asokpant@gmail.com"  # TODO
        # recipient_email = row.get("email", None)
        if not recipient_email:
            print(f"No email found for {name}. Skipping...")
            continue
        placeholders = {
            "name": name,
            "event": event_name
        }
        message = create_message(message_template, placeholders)
        certificate = row.get("output_file_url", None)
        email = EmailDetail(
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            message_type="markdown",
            attachments=[certificate]
        )
        success = email_service.send_email(email=email)
        df.at[index, "email_sent"] = success
        df.to_csv(certificates_csv, index=False)


def send_bca_internship_report_writing_certificate(email_service: EmailService):
    event_name = "National Webinar on BCA Project Report Writing"
    subject = f"Certificate of Participation - {event_name}"
    message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()
    certificates_csv = "data/certificates/20250517-webinar-bca-project-report/certificates.csv"
    df = pd.read_csv(certificates_csv)

    for index, row in df.iterrows():
        is_email_sent = row.get("email_sent", False)
        is_email_sent = False if pd.isna(is_email_sent) else bool(is_email_sent)

        if is_email_sent:
            print(f"Email already sent for {index}: {row.get('name', 'Participant')}. Skipping...")
            continue
        name = row.get("name", "Participant")
        recipient_email = "asokpant@gmail.com"
        # recipient_email = row.get("email", None)
        if not recipient_email:
            print(f"No email found for {name}. Skipping...")
            continue
        placeholders = {
            "name": name,
            "event": event_name
        }
        message = create_message(message_template, placeholders)
        certificate = row.get("output_file_url", None)
        email = EmailDetail(
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            message_type="markdown",
            attachments=[certificate]
        )
        success = email_service.send_email(email=email)
        df.at[index, "email_sent"] = success
        df.to_csv(certificates_csv, index=False)


def send_wifi_webinar_certificate(email_service: EmailService):
    event_name = "Live Webinar on WiFi Applications: Opportunities and Challenges in Nepalese Context"
    subject = f"Certificate of Participation - {event_name}"
    message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()
    certificates_csv = "data/certificates/20250614-webinar-wifi/certificates.csv"
    df = pd.read_csv(certificates_csv)

    for index, row in df.iterrows():
        is_email_sent = row.get("email_sent", False)
        is_email_sent = False if pd.isna(is_email_sent) else bool(is_email_sent)

        if is_email_sent:
            print(f"Email already sent for {index}: {row.get('name', 'Participant')}. Skipping...")
            continue
        name = row.get("name", "Participant")
        # recipient_email = "asokpant@gmail.com"
        recipient_email = row.get("email", None)
        if not recipient_email:
            print(f"No email found for {name}. Skipping...")
            continue
        placeholders = {
            "name": name,
            "event": event_name
        }
        message = create_message(message_template, placeholders)
        certificate = row.get("output_file_url", None)
        email = EmailDetail(
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            message_type="markdown",
            attachments=[certificate]
        )
        success = email_service.send_email(email=email)
        df.at[index, "email_sent"] = success
        df.to_csv(certificates_csv, index=False)


async def send_wifi_webinar_certificate_async():
    email_service = EmailServiceAsync()
    await email_service.connect()
    event_name = "Live Webinar on WiFi Applications: Opportunities and Challenges in Nepalese Context"
    subject = f"Certificate of Participation - {event_name}"
    message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()
    certificates_csv = "data/certificates/20250614-webinar-wifi/certificates.csv"
    df = pd.read_csv(certificates_csv)

    emails = []
    for index, row in df.iterrows():
        is_email_sent = row.get("email_sent", False)
        is_email_sent = False if pd.isna(is_email_sent) else bool(is_email_sent)

        if is_email_sent:
            print(f"Email already sent for {index}: {row.get('name', 'Participant')}. Skipping...")
            continue
        name = row.get("name", "Participant")
        recipient_email = "asokpant@gmail.com"
        # recipient_email = row.get("email", None)
        if not recipient_email:
            print(f"No email found for {name}. Skipping...")
            continue
        placeholders = {
            "name": name,
            "event": event_name
        }
        message = create_message(message_template, placeholders)
        certificate = row.get("output_file_url", None)
        email = EmailDetail(
            recipient_email=recipient_email,
            subject=subject,
            message=message,
            message_type="markdown",
            attachments=[certificate]
        )
        emails.append((index, email))
        if len(emails) % 10 == 0:
            results = await email_service.send_in_batch(emails=emails)
            for index_, status_ in results:
                df.at[index_, "email_sent"] = status_
            df.to_csv(certificates_csv, index=False)
            emails = []

    if len(emails) > 0:
        results = await email_service.send_in_batch(emails=emails)
        for index_, status_ in results:
            df.at[index_, "email_sent"] = status_
        df.to_csv(certificates_csv, index=False)


if __name__ == '__main__':
    # email_service = EmailService()
    # send_csit_internship_report_writing_certificate(email_service=email_service)
    # send_bca_internship_report_writing_certificate(email_service)
    # send_wifi_webinar_certificate(email_service=email_service)
    asyncio.run(send_wifi_webinar_certificate_async())
