from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSON
from certificateservice.model.base import Base

class TemplateRecord(Base):
    __tablename__ = "template"

    template_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    placeholders = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

