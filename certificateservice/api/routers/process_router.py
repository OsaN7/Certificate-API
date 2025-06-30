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

@router.post("/add", summary="Add Certificate Process")
def add_certificate_process(req: AddProcessRequest = Body(...), response_model=AddProcessResponse):
    try:
        return process_service.add_certificate_process(req)
    except Exception as e:
        logger.error(e)
        return AddProcessResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.get("/list", summary="List Certificate Processes")
def list_certificate_processes(user_id: str, response_model=ListProcessesResponse):
    """List all certificate processes for a user."""
    try:
        return process_service.list_process(user_id)
    except Exception as e:
        logger.error(e)
        return AddProcessResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))
