from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: Optional[str] = None
    full_name: str = None
    username: str = None
    email: str = None

    class Config:
        from_attributes = True  # allows reading data from ORM objects
