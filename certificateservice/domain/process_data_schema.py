from typing import Optional
from datetime import datetime
from pydantic import Field
from pydantic import BaseModel


class ProcessDataSchema(BaseModel):
    process_data_id: Optional[str] = None
    name: str 
    user_id: Optional[str] = None
    process_id: Optional[str] = None
    # created_at: datetime = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
