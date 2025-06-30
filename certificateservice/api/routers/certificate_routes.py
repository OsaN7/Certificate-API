import traceback
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from certificateservice.repo.certificate_repo import CertificateProcessRepo
from certificateservice.repo.datasource import DataSource, get_db
from certificateservice.service.certificate_service import CertificateService
from certificateservice.utils import loggerutil

router = APIRouter(prefix="/certificates")

db = DataSource()
repo = CertificateProcessRepo(db=db)
certificate_service = CertificateService(repo=repo)
logger = loggerutil.get_logger(__name__)

# --- Certificate Process Management ---

@router.post("/process", tags=["Add Certificate Process"], summary="Add Certificate Process")
def add_certificate_process(
        name: str = Body(..., description="Certificate process name"),
        date: str = Body(..., description="Date of the process (YYYY-MM-DD)"),
        user_id: str = Body(..., description="User ID"),
):
    """Add a new certificate process."""
    try:
        return certificate_service.add_certificate_process(name, date, user_id)
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/processes", tags=["Add Certificate Process"], summary="List Certificate Processes")
def list_certificate_processes(user_id: str = Query(..., description="User ID to list certificate processes for")):
    """List all certificate processes for a user."""
    try:
        return certificate_service.list_certificate_processes(user_id)
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
