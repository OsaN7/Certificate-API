"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/06/2025
"""

from fastapi import APIRouter, Body

from certificateservice.domain.common import ErrorCode
from certificateservice.domain.process_reqres import AddProcessRequest, AddProcessResponse, ListProcessesResponse
from certificateservice.repo.datasource import DataSource
from certificateservice.repo.process_repo import ProcessRepo
from certificateservice.service.process_service import ProcessService
from certificateservice.utils import loggerutil

router = APIRouter(prefix="/process", tags=["Process Management"])

db = DataSource()
process_repo = ProcessRepo(db=db)
process_service = ProcessService(process_repo=process_repo)
logger = loggerutil.get_logger(__name__)


# --- Certificate Process Management ---

@router.post("/add", summary="Add Certificate Process", response_model=AddProcessResponse)
def add_certificate_process(req: AddProcessRequest = Body(...)):
    try:
        return process_service.add_certificate_process(req)
    except Exception as e:
        logger.error(e)
        return AddProcessResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.get("/list", summary="List Certificate Processes", response_model=ListProcessesResponse)
def list_certificate_processes(user_id: str):
    """List all certificate processes for a user."""
    try:
        return process_service.list_process(user_id)
    except Exception as e:
        logger.error(e)
        return ListProcessesResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.delete("/delete/", summary="Delete Certificate Process")
def delete_certificate_process(process_id: str):
    """Delete a certificate process for a user."""
    try:
        result = process_service.delete_process(process_id)
        if result:
            return {"success": True, "message": "Certificate process deleted successfully."}
        else:
            return {"success": False, "message": "No process found with the given ID."}
    except Exception as e:
        logger.error(e)
        return {"success": False, "message": "Certificate process UNABLE to delete."}