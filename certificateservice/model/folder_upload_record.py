from sqlalchemy import Column, DateTime, String, func, LargeBinary
from certificateservice.model.base import Base
import uuid

class FolderUploadRecord(Base):
    __tablename__ = "folder_uploads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    folder_name = Column(String, nullable=False, index=True)
    template_file = Column(LargeBinary, nullable=False)
    csv_file = Column(LargeBinary, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_id = Column(String, nullable=True, index=True)  # Optional user association 