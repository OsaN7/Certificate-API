# """
# -- Created by: Ashok Kumar Pant
# -- Email: asokpant@gmail.com
# -- Created on: 17/06/2025
# """
# from textwrap import dedent

# import pandas as pd
# from pydantic import BaseModel

# from certificateservice.service.email_service import EmailService


# def create_message(template: str, placeholders: dict) -> str:
#     """
#     Generate a message from a template and placeholders.
#     """
#     if not template:
#         return ""
#     if not placeholders:
#         return template
#     return template.format(**placeholders)


# PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE = """
#         Dear {name},

#         Thank you for participating in the **{event}**.  
#         We truly appreciate your involvement and enthusiasm.

#         Please find your certificate of participation attached.

#         Best regards,  
#         **Pascal College, Lalitpur, Nepal**  
#         *A College Run by IT Professionals*  
#         Phone: +977 15916910  
#         Website: [www.pascalcollege.edu.np](https://www.pascalcollege.edu.np/)  

#         **Connect with us:**  
#         [Facebook](https://www.facebook.com/pascal.national.college) | [YouTube](https://www.youtube.com/@pascal.national.college) | [X (Twitter)](https://x.com/pascal_college)  
#         [LinkedIn](https://www.linkedin.com/company/pascalcollege) | [Instagram](https://www.instagram.com/pascal.college/) | [TikTok](https://www.tiktok.com/@pascalcollege)
#     """


# class EmailDetail(BaseModel):
#     recipient_email: str
#     subject: str
#     message: str
#     message_type: str
#     attachments: list[str] = None


<<<<<<< HEAD
# def send_email(email_service: EmailService, emails: list[EmailDetail]):
#     try:
#         for email in emails:
#             email_service.send(
#                 recipient_emails=email.recipient_email,
#                 subject=email.subject,
#                 message=email.message,
#                 attachments=email.attachments,
#                 message_type=email.message_type
#             )
#             print(f"Email sent to {email.recipient_email} with subject: {email.subject}")
#     except Exception as e:
#         print(f"Failed to send email: {e}")
=======
def send_email(email_service: EmailService, emails: list[EmailDetail]) -> bool:
    try:
        for email in emails:
            success = email_service.send(
                recipient_emails=email.recipient_email,
                subject=email.subject,
                message=email.message,
                attachments=email.attachments,
                message_type=email.message_type
            )
            if not success:
                return False
            print(f"Email sent to {email.recipient_email} with subject: {email.subject}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
>>>>>>> 5e7812957d3de35b9b1d1c57dcad3ffbd9c836da


# def send_email_example():
#     email_service = EmailService()
#     subject = "Certificate of Participation for Webinar on B.Sc. CSIT Internship Report Writing"
#     message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()

<<<<<<< HEAD
#     placeholders = {
#         "name": "Nishma Gautam",
#         "event": "Webinar on CSIT Internship Report Writing"
#     }
#     message = create_message(message_template, placeholders)
#     email = EmailDetail(
#         recipient_email="asokpant@gmail.com",
#         subject=subject,
#         message=message,
#         message_type="markdown",
#         attachments=[
#             "data/certificates/20250510-webinar-csit-internship-report/20250510-webinar-080bca13.nishma@scst.edu.np-Nishma Gautam.pdf"]
#     )
#     send_email(email_service, emails=[email])
=======
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
    success = send_email(email_service, emails=[email])
    print(f"Email sent to {email.recipient_email} with subject: {email.subject}")
>>>>>>> 5e7812957d3de35b9b1d1c57dcad3ffbd9c836da


# def send_csit_internship_report_writing_certificate(email_service: EmailService):
#     event_name = "National Webinar on B.Sc. CSIT Internship Report Writing"
#     subject = f"Certificate of Participation - {event_name}"
#     message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()
#     certificates_csv = "data/certificates/20250510-webinar-csit-internship-report/certificates.csv"
#     df = pd.read_csv(certificates_csv)

#     for index, row in df.iterrows():
#         is_email_sent = row.get("email_sent", False)
#         is_email_sent = False if pd.isna(is_email_sent) else bool(is_email_sent)

<<<<<<< HEAD
#         if is_email_sent:
#             print(f"Email already sent for {index}: {row.get('name', 'Participant')}. Skipping...")
#             continue
#         name = row.get("name", "Participant")
#         recipient_email = row.get("email", None)
#         if not recipient_email:
#             print(f"No email found for {name}. Skipping...")
#             continue
#         placeholders = {
#             "name": name,
#             "event": event_name
#         }
#         message = create_message(message_template, placeholders)
#         certificate = row.get("output_file_url", None)
#         email = EmailDetail(
#             recipient_email=recipient_email,
#             subject=subject,
#             message=message,
#             message_type="markdown",
#             attachments=[certificate]
#         )
#         send_email(email_service, emails=[email])
#         df.at[index, "email_sent"] = True
#         df.to_csv(certificates_csv, index=False)
=======
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
        success = send_email(email_service, emails=[email])
        df.at[index, "email_sent"] = success
        df.to_csv(certificates_csv, index=False)
>>>>>>> 5e7812957d3de35b9b1d1c57dcad3ffbd9c836da


# def send_bca_internship_report_writing_certificate(email_service: EmailService):
#     event_name = "National Webinar on BCA Project Report Writing"
#     subject = f"Certificate of Participation - {event_name}"
#     message_template = dedent(PNC_CERTIFICATE_OF_PARTICIPATION_EMAIL_TEMPLATE).strip()
#     certificates_csv = "data/certificates/20250517-webinar-bca-project-report/certificates.csv"
#     df = pd.read_csv(certificates_csv)

#     for index, row in df.iterrows():
#         is_email_sent = row.get("email_sent", False)
#         is_email_sent = False if pd.isna(is_email_sent) else bool(is_email_sent)

<<<<<<< HEAD
#         if is_email_sent:
#             print(f"Email already sent for {index}: {row.get('name', 'Participant')}. Skipping...")
#             continue
#         name = row.get("name", "Participant")
#         recipient_email = "asokpant@gmail.com"  # row.get("email", None)
#         placeholders = {
#             "name": name,
#             "event": event_name
#         }
#         message = create_message(message_template, placeholders)
#         certificate = row.get("output_file_url", None)
#         email = EmailDetail(
#             recipient_email=recipient_email,
#             subject=subject,
#             message=message,
#             message_type="markdown",
#             attachments=[certificate]
#         )
#         send_email(email_service, emails=[email])
#         df.at[index, "email_sent"] = True
#         df.to_csv(certificates_csv, index=False)


# if __name__ == '__main__':
#     email_service = EmailService()
#     send_csit_internship_report_writing_certificate(email_service=email_service)
#     # send_bca_internship_report_writing_certificate(email_service)
=======
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
        success = send_email(email_service, emails=[email])
        df.at[index, "email_sent"] = success
        df.to_csv(certificates_csv, index=False)


if __name__ == '__main__':
    email_service = EmailService()
    # send_csit_internship_report_writing_certificate(email_service=email_service)
    send_bca_internship_report_writing_certificate(email_service)
>>>>>>> 5e7812957d3de35b9b1d1c57dcad3ffbd9c836da
