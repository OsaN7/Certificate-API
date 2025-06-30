import traceback
import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, Body, Query, UploadFile, File
from sqlalchemy.orm import Session
from certificateservice.repo.process_template_repo import ProcessTemplateRepo
from certificateservice.repo.datasource import get_db

from certificateservice.service.process_template_service import ProcessTemplateService
from certificateservice.utils import loggerutil

router = APIRouter(prefix="/certificates/process-template")
logger = loggerutil.get_logger(__name__)

def get_process_template_service(db: Session = Depends(get_db)):
    repo = ProcessTemplateRepo(db)
    return ProcessTemplateService(repo=repo, db=db)

@router.post("/process/template", tags=["Process Template Page"], summary="Add Process Template")
def add_process_template(
        name: str = Body(..., description="Template name"),
        user_id: str = Body(..., description="User ID"),
        process_id: str = Body(None, description="Process ID (optional, will be generated if not provided)"),
        template_file: UploadFile = File(..., description="Template file (PDF)"),
        service: ProcessTemplateService = Depends(get_process_template_service)
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
        service: ProcessTemplateService = Depends(get_process_template_service)
):
    try:
        return service.list_process_templates(user_id, process_id)
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/process/template/download", tags=["Process Template Page"], summary="Download Process Template PDF")
def download_process_template(template_id: str = Query(..., description="Template ID"), service: ProcessTemplateService = Depends(get_process_template_service)):
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
def delete_process_template(template_id: str = Query(..., description="Template ID"), service: ProcessTemplateService = Depends(get_process_template_service)):
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
def test_template_url(template_id: str = Query(..., description="Template ID"), service: ProcessTemplateService = Depends(get_process_template_service)):
    try:
        return service.test_template_url(template_id)
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
