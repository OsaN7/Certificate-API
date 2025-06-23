from datetime import datetime
from pydantic import BaseModel


class course_record(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

