from pydantic import BaseModel

class BulkEmailRequest(BaseModel):
    process_data_id: str
    subject: str
    body: str
    test_email: str = None  # Optional test email
