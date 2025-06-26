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

class CertificateProcessSchema(BaseModel):
    process_id: str
    name: str
    date: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# class ProcessTemplateSchema(BaseModel):
#     template_id: str
#     name: str
#     user_id: str
#     process_id: str
#     template_file: str
#     created_at: datetime

#     class Config:
#         from_attributes = True

# class ProcessDataSchema(BaseModel):
#     process_data_id: str
#     name: str
#     user_id: str
#     process_id: str
#     created_at: datetime

#     class Config:
#         from_attributes = True
