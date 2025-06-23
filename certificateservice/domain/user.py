from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: Optional[str] = None
    full_name: str=None
    username: str=None
    email: str=None

    class Config:
        # For Pydantic v2, use `from_attributes` instead of `orm_mode`
        from_attributes = True  # allows reading data from ORM objects
