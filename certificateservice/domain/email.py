from pydantic import BaseModel


class BulkEmailRequest(BaseModel):
    process_data_id: str
    subject: str
    body: str
    test_email: str = None  # Optional test email


class EmailDetail(BaseModel):
    recipient_email: str
    subject: str
    message: str
    message_type: str
    attachments: list[str] = None
