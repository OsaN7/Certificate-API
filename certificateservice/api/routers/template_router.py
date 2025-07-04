from fastapi import APIRouter, Body, UploadFile, File, Form
from certificateservice.domain.common import ErrorCode
from certificateservice.domain.process_template_reqres import (
    AddTemplateRequest,
    AddTemplateResponse,
    ListTemplateResponse,
    DeleteTemplateResponse,
)
from certificateservice.repo.datasource import DataSource
from certificateservice.repo.process_template_repo import ProcessTemplateRepo
from certificateservice.service.process_template_service import ProcessTemplateService
from certificateservice.utils import loggerutil

router = APIRouter(prefix="/certificates/process-template", tags=["Process Template Management"])
logger = loggerutil.get_logger(__name__)

db = DataSource()
repo = ProcessTemplateRepo(db=db)
service = ProcessTemplateService(repo=repo)


@router.post("/add", summary="Add Process Template", response_model=AddTemplateResponse)
def add_process_template(req: AddTemplateRequest = Body(...)):
    try:
        return service.add_process_template(req)
    except Exception as e:
        logger.error(e)
        return AddTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

@router.get("/list", summary="List Process Templates", response_model=ListTemplateResponse)
def list_process_templates(user_id: str = None, process_id: str = None):
    try:
        return service.list_process_templates(user_id=user_id, process_id=process_id)
    except Exception as e:
        logger.error(e)
        return ListTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.delete("/delete", summary="Delete Process Template", response_model=DeleteTemplateResponse)
def delete_process_template(template_id: str):
    try:
        result = service.delete_process_template(template_id)
        if result is None:
            return DeleteTemplateResponse(error=True, error_code=ErrorCode.NOT_FOUND, msg="Template not found")
        return result
    except Exception as e:
        logger.error(e)
        return DeleteTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))
