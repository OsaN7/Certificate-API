import traceback

from fastapi import APIRouter, HTTPException, Body, Query, UploadFile, File

from certificateservice.repo.datasource import DataSource
from certificateservice.repo.process_template_repo import ProcessTemplateRepo
from certificateservice.service.process_template_service import ProcessTemplateService
from certificateservice.utils import loggerutil

router = APIRouter(prefix="/certificates/process-template")
logger = loggerutil.get_logger(__name__)

db = DataSource()
repo = ProcessTemplateRepo(db)
service = ProcessTemplateService(repo=repo)


@router.post("/process/template", tags=["Process Template Page"], summary="Add Process Template")
def add_process_template(
        name: str = Body(..., description="Template name"),
        user_id: str = Body(..., description="User ID"),
        process_id: str = Body(None, description="Process ID (optional, will be generated if not provided)"),
        template_file: UploadFile = File(..., description="Template file (PDF)"),
):
    try:
        return service.add_process_template(name, user_id, process_id, template_file)
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/templates", tags=["Process Template Page"], summary="List Process Templates")
def list_process_templates(
        user_id: str = Query(..., description="User ID"),
        process_id: str = Query(..., description="Process ID"),
):
    try:
        return service.list_process_templates(user_id, process_id)
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/template/download", tags=["Process Template Page"], summary="Download Process Template PDF")
def download_process_template(template_id: str = Query(..., description="Template ID")):
    try:
        response = service.download_process_template(template_id)
        if response is None:
            raise HTTPException(status_code=404, detail="Template not found")
        return response
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/process/template", tags=["Process Template Page"], summary="Delete Process Template")
def delete_process_template(template_id: str = Query(..., description="Template ID")):
    try:
        result = service.delete_process_template(template_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Template not found")
        return result
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/template/test-url", tags=["Process Template Page"], summary="Test Template URL")
def test_template_url(template_id: str = Query(..., description="Template ID")):
    try:
        return service.test_template_url(template_id)
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
