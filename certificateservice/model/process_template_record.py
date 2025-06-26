from sqlalchemy import Column, String, DateTime, func, LargeBinary
from certificateservice.model.base import Base

class ProcessTemplateRecord(Base):
    __tablename__ = "process_template"

    template_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(String, nullable=False, index=True)
    process_id = Column(String, nullable=False, index=True)
    template_file = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, server_default=func.now()) 