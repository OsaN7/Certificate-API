from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from certificateservice.repo.datasource import get_db
from certificateservice.repo.folder_upload_repo import FolderUploadRepo
from certificateservice.service.folder_upload_service import FolderUploadService
from certificateservice.domain.folder_upload import FolderUploadResponse, FolderUploadStatusResponse
from certificateservice.utils import loggerutil
from fastapi.responses import StreamingResponse

logger = loggerutil.get_logger(__name__)

router = APIRouter(prefix="/folder-uploads", tags=["Folder Uploads"])

def get_repo(db: Session) -> FolderUploadRepo:
    return FolderUploadRepo(db)

def get_service(db: Session) -> FolderUploadService:
    repo = get_repo(db)
    return FolderUploadService(repo)

@router.get("/", response_model=List[FolderUploadResponse])
async def list_uploads(
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all folder uploads, optionally filtered by user_id"""
    try:
        service = get_service(db)
        uploads = service.get_all_uploads(user_id)
        
        return [
            FolderUploadResponse(
                id=upload.id,
                folder_name=upload.folder_name,
                template_file=upload.template_file,
                csv_file=upload.csv_file,
                status=upload.status,
                error_message=upload.error_message,
                created_at=upload.created_at,
                updated_at=upload.updated_at,
                user_id=upload.user_id
            )
            for upload in uploads
        ]
    except Exception as e:
        logger.error(f"Error in list_uploads endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{upload_id}")
async def delete_upload(
    upload_id: str,
    db: Session = Depends(get_db)
):
    """Delete a folder upload by ID"""
    try:
        service = get_service(db)
        success = service.delete_upload(upload_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Upload not found")
        
        return {"message": "Upload deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_upload endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/upload-files", response_model=FolderUploadResponse)
async def upload_files(
    folder_name: str = Form(..., description="Name of the folder"),
    template_file: UploadFile = File(..., description="PDF template file"),
    csv_file: UploadFile = File(..., description="CSV data file"),
    user_id: Optional[str] = Form(None, description="Optional user ID"),
    db: Session = Depends(get_db)
):
    service = get_service(db)
    folder_upload = service.process_files_upload(folder_name, template_file, csv_file, user_id)
    return FolderUploadResponse(
        id=folder_upload.id,
        folder_name=folder_upload.folder_name,
        template_file=folder_upload.template_file,
        csv_file=folder_upload.csv_file,
        status=folder_upload.status,
        error_message=folder_upload.error_message,
        created_at=folder_upload.created_at,
        updated_at=folder_upload.updated_at,
        user_id=folder_upload.user_id
    )

@router.get("/{upload_id}/download-template")
async def download_template(upload_id: str, db: Session = Depends(get_db)):
    service = get_service(db)
    folder_upload = service.get_upload_status(upload_id)
    if not folder_upload or not folder_upload.template_file:
        raise HTTPException(status_code=404, detail="Template file not found")
    return StreamingResponse(
        iter([folder_upload.template_file]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=template_{upload_id}.pdf"}
    )

@router.get("/{upload_id}/download-csv")
async def download_csv(upload_id: str, db: Session = Depends(get_db)):
    service = get_service(db)
    folder_upload = service.get_upload_status(upload_id)
    if not folder_upload or not folder_upload.csv_file:
        raise HTTPException(status_code=404, detail="CSV file not found")
    return StreamingResponse(
        iter([folder_upload.csv_file]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data_{upload_id}.csv"}
    ) 

"""In Psql we can use the following to download the template and csv files:


SELECT   id,   octet_length(template_file) AS template_file_size,   octet_length(csv_file) AS csv_fil
e_size FROM folder_uploads;

"""