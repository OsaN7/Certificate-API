from sqlalchemy import Column, DateTime, String, func
from certificateservice.model.base import Base

class UserRecord(Base):
    __tablename__= "user"

    user_id = Column(String, primary_key=True)
    full_name=Column(String,nullable=False)
    username=Column(String,nullable=False)
    email=Column(String,unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at=Column(DateTime,server_default=func.now())
    updated_at=Column(DateTime,server_default=func.now(),onupdate=func.now())

