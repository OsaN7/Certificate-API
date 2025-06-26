from sqlalchemy import Column, String, DateTime, func
from certificateservice.model.base import Base

class CertificateProcessRecord(Base):
    __tablename__ = "certificate_process"

    process_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now()) 