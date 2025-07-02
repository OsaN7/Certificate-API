from fastapi import APIRouter, Body, Query, UploadFile, File
from certificateservice.domain.common import ErrorCode
from certificateservice.domain.process_template_reqres import (
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


@router.post("/add", summary="Add Process Template")
def add_process_template(
    name: str = Body(..., description="Template name"),
    user_id: str = Body(..., description="User ID"),
    process_id: str = Body(None, description="Optional process ID"),
    template_file: UploadFile = File(..., description="PDF Template File"),
) -> AddTemplateResponse:
    try:
        return service.add_process_template(name, user_id, process_id, template_file)
    except Exception as e:
        logger.error(e)
        return AddTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.get("/list", summary="List Process Templates")
def list_process_templates(
    user_id: str = Query(..., description="User ID"),
    process_id: str = Query(..., description="Process ID"),
) -> ListTemplateResponse:
    try:
        return service.list_process_templates(user_id, process_id)
    except Exception as e:
        logger.error(e)
        return ListTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.get("/download", summary="Download Process Template PDF")
def download_process_template(template_id: str = Query(..., description="Template ID")):
    try:
        response = service.download_process_template(template_id)
        if response is None:
            return {"error": True, "error_code": ErrorCode.NOT_FOUND, "msg": "Template not found"}
        return response
    except Exception as e:
        logger.error(e)
        return {"error": True, "error_code": ErrorCode.INTERNAL_ERROR, "msg": str(e)}


@router.delete("/delete", summary="Delete Process Template")
def delete_process_template(template_id: str = Query(..., description="Template ID")) -> DeleteTemplateResponse:
    try:
        result = service.delete_process_template(template_id)
        if result is None:
            return DeleteTemplateResponse(error=True, error_code=ErrorCode.NOT_FOUND, msg="Template not found")
        return result
    except Exception as e:
        logger.error(e)
        return DeleteTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


@router.get("/test-url", summary="Test Template URL")
def test_template_url(template_id: str = Query(..., description="Template ID")):
    try:
        return service.test_template_url(template_id)
    except Exception as e:
        logger.error(e)
        return {"error": True, "error_code": ErrorCode.INTERNAL_ERROR, "msg": str(e)}
