import os
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException, File, Form, APIRouter, Depends
from fastapi.responses import StreamingResponse
from certificateservice.repo.folder_upload_repo import FolderUploadRepo
from certificateservice.model.folder_upload_record import FolderUploadRecord
from certificateservice.utils import loggerutil
import pandas as pd
import io
from sqlalchemy.orm import Session
from certificateservice.repo.datasource import get_db

logger = loggerutil.get_logger(__name__)

class FolderUploadService:
    def __init__(self, repo: FolderUploadRepo):
        self.repo = repo
        self.logger = logger
        self.upload_base_dir = "data/uploads"
        self.template_dir = "data/templates"
        self.csv_dir = "data/csv"

    def process_folder_upload(self, folder_name: str, template_file: UploadFile, csv_file: UploadFile, user_id: Optional[str] = None) -> FolderUploadRecord:
        """Process folder upload from zip file"""
        try:
            # Validate file types
            if not template_file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Template file must be a PDF")
            if not csv_file.filename.endswith('.csv'):
                raise HTTPException(status_code=400, detail="CSV file must be a CSV")

            self._ensure_directories()

            # Read file contents
            template_bytes = template_file.file.read()
            csv_bytes = csv_file.file.read()

            # Create database record
            folder_upload = self.repo.create_folder_upload(
                folder_name=folder_name,
                template_file=template_bytes,
                csv_file=csv_bytes,
                user_id=user_id
            )

            # Update status to processing
            self.repo.update_folder_upload_status(folder_upload.id, "processing")

            # Process the files (generate certificates)
            try:
                self._process_certificates(folder_upload)
                self.repo.update_folder_upload_status(folder_upload.id, "completed")
            except Exception as e:
                error_msg = f"Error processing certificates: {str(e)}"
                self.logger.error(error_msg)
                self.repo.update_folder_upload_status(folder_upload.id, "failed", error_msg)
                raise HTTPException(status_code=500, detail=error_msg)

            return folder_upload

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error processing folder upload: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.upload_base_dir, exist_ok=True)
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.csv_dir, exist_ok=True)

    def _process_certificates(self, folder_upload: FolderUploadRecord):
        """Process certificates using the uploaded template and CSV"""
        try:
            # Read CSV data from bytes
            csv_bytes = folder_upload.csv_file
            df = pd.read_csv(io.BytesIO(csv_bytes))
            
            # Basic validation of CSV structure
            if df.empty:
                raise Exception("CSV file is empty")

            # Check for required columns (name and email)
            required_columns = ['name', 'email']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise Exception(f"CSV file missing required columns: {missing_columns}")

            # Create output directory for certificates
            output_dir = os.path.join("data/certificates", folder_upload.folder_name)
            os.makedirs(output_dir, exist_ok=True)

            # Here you would integrate with your existing certificate generation logic
            # For now, we'll just log the processing
            self.logger.info(f"Processing {len(df)} certificates for folder: {folder_upload.folder_name}")
            self.logger.info(f"Template: [binary PDF in DB]")
            self.logger.info(f"CSV: [binary CSV in DB]")
            self.logger.info(f"Output directory: {output_dir}")

            # TODO: Integrate with your existing certificate generation logic from main.py
            # This would involve calling the certificate generation functions with the uploaded files

        except Exception as e:
            self.logger.error(f"Error processing certificates: {e}")
            raise

    def get_upload_status(self, upload_id: str) -> Optional[FolderUploadRecord]:
        """Get upload status by ID"""
        return self.repo.get_folder_upload_by_id(upload_id)

    def get_all_uploads(self, user_id: Optional[str] = None) -> list[FolderUploadRecord]:
        """Get all uploads for a user"""
        return self.repo.get_all_folder_uploads(user_id)

    def delete_upload(self, upload_id: str) -> bool:
        """Delete upload by ID"""
        return self.repo.delete_folder_upload(upload_id)

    def _ensure_upload_base_dir(self):
        os.makedirs("data/uploads", exist_ok=True)

    def process_files_upload(self, folder_name: str, template_file: UploadFile, csv_file: UploadFile, user_id: Optional[str] = None):
        self._ensure_upload_base_dir()
        # Read file contents
        template_bytes = template_file.file.read()
        csv_bytes = csv_file.file.read()

        # Create DB record
        folder_upload = self.repo.create_folder_upload(
            folder_name=folder_name,
            template_file=template_bytes,
            csv_file=csv_bytes,
            user_id=user_id
        )
        return folder_upload

router = APIRouter()

@router.get("/folder-uploads/{upload_id}/download-template")
def download_template(upload_id: str, db: Session = Depends(get_db)):
    repo = FolderUploadRepo(db)
    folder_upload = repo.get_folder_upload_by_id(upload_id)
    if not folder_upload or not folder_upload.template_file:
        raise HTTPException(status_code=404, detail="File not found")
    return StreamingResponse(
        iter([folder_upload.template_file]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=template_{upload_id}.pdf"}
    ) 