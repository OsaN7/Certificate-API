from fastapi import APIRouter, Depends, HTTPException, Body, Query, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
import traceback
import shutil
import io
import csv
from pydantic import BaseModel
from certificateservice.domain.email import BulkEmailRequest
from certificateservice.model.process_data_record import ProcessDataRecord
from certificateservice.repo.datasource import get_db
from certificateservice.service.email_service import send_email_to_list

router = APIRouter(prefix="/certificates/process", tags=["Process Data Page"])


@router.post("/process/data", tags=["Process Data Page"], summary="Add Process Data")
def add_process_data(
    name: str = Body(..., description="Process data name"),
    user_id: str = Body(..., description="User ID"),
    process_id: str = Body(None, description="Process ID (optional, will be generated if not provided)"),
    csv_file: UploadFile = File(..., description="CSV file"),
    db: Session = Depends(get_db)
):
    try:
        if not process_id:
            process_id = str(uuid.uuid4())
        process_data_id = str(uuid.uuid4())

        file_bytes = csv_file.file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        data_dir = os.path.join(base_dir, process_data_id)
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, csv_file.filename)
        with open(csv_path, "wb") as f:
            f.write(file_bytes)

        process_data_record = ProcessDataRecord(
            process_data_id=process_data_id,
            name=name,
            user_id=user_id,
            process_id=process_id,
            csv_file=file_bytes
        )
        db.add(process_data_record)
        db.commit()
        db.refresh(process_data_record)

        return {
            "process_data_id": process_data_id,
            "name": name,
            "user_id": user_id,
            "process_id": process_id,
            "csv_file": csv_file.filename
        }
    except Exception as e:
        print("ERROR during add_process_data:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/data/url", tags=["Process Data Page"], summary="List Process Data URLs")
def list_process_data_urls(user_id: str = Query(..., description="User ID")):
    try:
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        urls = []
        for folder in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.lower().endswith('.csv'):
                        url = f"/data/{folder}/{file}"
                        urls.append({"process_data_id": folder, "csv_file": file, "url": url})
        return urls
    except Exception as e:
        print("ERROR during list_process_data_urls:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/process/data", tags=["Process Data Page"], summary="Delete Process Data")
def delete_process_data(process_data_id: str = Query(..., description="process_data_id"), db: Session = Depends(get_db)):
    try:
        data = db.query(ProcessDataRecord).filter_by(process_data_id=process_data_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Data not found")

        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        data_dir = os.path.join(base_dir, process_data_id)
        if os.path.isdir(data_dir):
            shutil.rmtree(data_dir)

        db.delete(data)
        db.commit()
        return {"message": "Data deleted successfully", "data_id": process_data_id}
    except Exception as e:
        print("ERROR during delete_process_data:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process/data/send-emails", tags=["Process Data Page"], summary="Send Emails Using CSV")
async def send_emails_from_csv(data: BulkEmailRequest, db: Session = Depends(get_db)):
    print(f"[DEBUG] Looking for process_data_id: {data.process_data_id}")
    record = db.query(ProcessDataRecord).filter_by(process_data_id=data.process_data_id).first()
    
    if not record:
        print(f"[ERROR] Process data not found for ID: {data.process_data_id}")
        raise HTTPException(status_code=404, detail="Process data not found")

    try:
        csv_bytes = record.csv_file
        if not csv_bytes:
            raise HTTPException(status_code=400, detail="No CSV data found in record.")
        
        csv_io = io.StringIO(csv_bytes.decode("utf-8"))
        reader = csv.DictReader(csv_io)

        sent, failed = await send_email_to_list(reader, data.subject, data.body, data.test_email)

        return {
            "test_email_sent_to": data.test_email,
            "emails_sent": sent,
            "emails_failed": failed,
            "total": len(sent) + len(failed)
        }
    except Exception as e:
        print("ERROR during send_emails_from_csv:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to send emails: {str(e)}")
