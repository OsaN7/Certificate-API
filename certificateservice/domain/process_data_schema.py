from datetime import datetime
from pydantic import BaseModel


class ProcessDataSchema(BaseModel):
    process_data_id: str
    name: str
    user_id: str
    process_id: str
    created_at: datetime

    class Config:
        from_attributes = True
