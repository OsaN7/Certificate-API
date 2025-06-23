from pydantic import BaseModel
from datetime import datetime

class CertificateRecordSchema(BaseModel):
    id: str
    user_id: str
    course_name: str
    issue_date: datetime
    certificate_url: str

    class Config:
        from_attributes = True
