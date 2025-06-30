import traceback
from fastapi import APIRouter, Depends, HTTPException, Body, Query, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
import shutil
import io
import csv
from pydantic import BaseModel
from certificateservice.domain.email import BulkEmailRequest
from certificateservice.model.process_data_record import ProcessDataRecord
from certificateservice.repo.datasource import DataSource, get_db
from certificateservice.service.process_data_service import ProcessDataService
from certificateservice.service.email_service import send_email_to_list
from certificateservice.utils import loggerutil

router = APIRouter(prefix="/certificates/process-data", tags=["Process Data Page"])

db = DataSource().get_session()
process_data_service = ProcessDataService(db=db)
logger = loggerutil.get_logger(__name__)


@router.post("/process/data", tags=["Process Data Page"], summary="Add Process Data")
def add_process_data(
    name: str = Body(..., description="Process data name"),
    user_id: str = Body(..., description="User ID"),
    process_id: str = Body(None, description="Process ID (optional, will be generated if not provided)"),
    csv_file: UploadFile = File(..., description="CSV file")
):
    try:
        return process_data_service.add_process_data(name, user_id, process_id, csv_file)
    except Exception as e:
        logger.error(e)
        print("ERROR during add_process_data:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/data/url", tags=["Process Data Page"], summary="List Process Data URLs")
def list_process_data_urls(user_id: str = Query(..., description="User ID")):
    try:
        return process_data_service.list_process_data_urls(user_id)
    except Exception as e:
        logger.error(e)
        print("ERROR during list_process_data_urls:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/process/data", tags=["Process Data Page"], summary="Delete Process Data")
def delete_process_data(process_data_id: str = Query(..., description="process_data_id")):
    try:
        return process_data_service.delete_process_data(process_data_id)
    except Exception as e:
        logger.error(e)
        print("ERROR during delete_process_data:", e)
        traceback.print_exc()
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/process/data/send-emails", tags=["Process Data Page"], summary="Send Emails Using CSV")
async def send_emails_from_csv(data: BulkEmailRequest, db: Session = Depends(get_db)):
    try:
        return await process_data_service.send_emails_from_csv(data, db)
    except Exception as e:
        logger.error(e)
        print("ERROR during send_emails_from_csv:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to send emails: {str(e)}")
