from datetime import datetime
from pydantic import BaseModel


class ProcessTemplateSchema(BaseModel):
    template_id: str
    name: str
    user_id: str
    process_id: str
    template_file: str
    created_at: datetime

    class Config:
        from_attributes = True