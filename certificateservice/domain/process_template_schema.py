from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ProcessTemplateSchema(BaseModel):
    template_id: Optional[str] = None
    name: str = None
    user_id: Optional[str] = None
    process_id: Optional[str] = None
    template_file: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True