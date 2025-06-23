from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FolderUploadRequest(BaseModel):
    folder_name: str
    user_id: Optional[str] = None

class FolderUploadResponse(BaseModel):
    id: str
    folder_name: str
    template_file: bytes
    csv_file: bytes
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str] = None

class FolderUploadStatusResponse(BaseModel):
    id: str
    status: str
    error_message: Optional[str] = None
    updated_at: datetime 