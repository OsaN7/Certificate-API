from pydantic import BaseModel
from datetime import datetime

class CertificateProcessSchema(BaseModel):
    process_id: str
    name: str
    date: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True
