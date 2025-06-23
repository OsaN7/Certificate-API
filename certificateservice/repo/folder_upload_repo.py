from sqlalchemy.orm import Session
from certificateservice.model.folder_upload_record import FolderUploadRecord
from certificateservice.domain.folder_upload import FolderUploadResponse, FolderUploadStatusResponse
from certificateservice.utils import loggerutil
from typing import List, Optional

logger = loggerutil.get_logger(__name__)

class FolderUploadRepo:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger

    def create_folder_upload(self, folder_name: str, template_file: bytes, csv_file: bytes, user_id: Optional[str] = None) -> FolderUploadRecord:
        """Create a new folder upload record"""
        try:
            folder_upload = FolderUploadRecord(
                folder_name=folder_name,
                template_file=template_file,
                csv_file=csv_file,
                user_id=user_id,
                status="pending"
            )
            self.db.add(folder_upload)
            self.db.commit()
            self.db.refresh(folder_upload)
            self.logger.info(f"Created folder upload record: {folder_upload.id}")
            return folder_upload
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error creating folder upload: {e}")
            raise

    def get_folder_upload_by_id(self, upload_id: str) -> Optional[FolderUploadRecord]:
        """Get folder upload by ID"""
        try:
            return self.db.query(FolderUploadRecord).filter(FolderUploadRecord.id == upload_id).first()
        except Exception as e:
            self.logger.error(f"Error getting folder upload by ID: {e}")
            raise

    def get_all_folder_uploads(self, user_id: Optional[str] = None) -> List[FolderUploadRecord]:
        """Get all folder uploads, optionally filtered by user_id"""
        try:
            query = self.db.query(FolderUploadRecord)
            if user_id:
                query = query.filter(FolderUploadRecord.user_id == user_id)
            return query.order_by(FolderUploadRecord.created_at.desc()).all()
        except Exception as e:
            self.logger.error(f"Error getting all folder uploads: {e}")
            raise

    def update_folder_upload_status(self, upload_id: str, status: str, error_message: Optional[str] = None) -> Optional[FolderUploadRecord]:
        """Update folder upload status"""
        try:
            folder_upload = self.get_folder_upload_by_id(upload_id)
            if folder_upload:
                folder_upload.status = status
                if error_message:
                    folder_upload.error_message = error_message
                self.db.commit()
                self.db.refresh(folder_upload)
                self.logger.info(f"Updated folder upload status: {upload_id} -> {status}")
                return folder_upload
            return None
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error updating folder upload status: {e}")
            raise

    def delete_folder_upload(self, upload_id: str) -> bool:
        """Delete folder upload by ID"""
        try:
            folder_upload = self.get_folder_upload_by_id(upload_id)
            if folder_upload:
                self.db.delete(folder_upload)
                self.db.commit()
                self.logger.info(f"Deleted folder upload: {upload_id}")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error deleting folder upload: {e}")
            raise 