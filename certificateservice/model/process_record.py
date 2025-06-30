from sqlalchemy import Column, String, DateTime, func

from certificateservice.model.base import Base


class ProcessRecord(Base):
    __tablename__ = "process"

    process_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
