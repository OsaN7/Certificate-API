import json
import os
import traceback
import uuid

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session

from certificateservice.repo.course_repo import CertificateProcessRepo

router = APIRouter(prefix="/certificates")


# --- Certificate Process Management ---

@router.post("/process", tags=["Add Certificate Process"], summary="Add Certificate Process")
def add_certificate_process(
        name: str = Body(..., description="Certificate process name"),
        date: str = Body(..., description="Date of the process (YYYY-MM-DD)"),
        user_id: str = Body(..., description="User ID"),
):
    """Add a new certificate process."""
    try:
        process_id = str(uuid.uuid4())
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        process_dir = os.path.join(base_dir, user_id, process_id)
        os.makedirs(process_dir, exist_ok=True)
        metadata = {
            "name": name,
            "date": date,
            "user_id": user_id,
            "process_id": process_id
        }
        with open(os.path.join(process_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f)
        repo = CertificateProcessRepo(db)
        repo.create_process({
            "process_id": process_id,
            "name": name,
            "date": date,
            "user_id": user_id
        })
        return {
            "message": "Certificate process created",
            "directory": os.path.relpath(process_dir, base_dir),
            "process_id": process_id
        }
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/processes", tags=["Add Certificate Process"], summary="List Certificate Processes")
def list_certificate_processes(user_id: str = Query(..., description="User ID to list certificate processes for"),
                               db: Session = Depends(get_db)):
    """List all certificate processes for a user."""
    try:
        repo = CertificateProcessRepo(db)
        processes = repo.get_processes_by_user(user_id)
        return [
            {
                "process_id": p.process_id,
                "name": p.name,
                "date": p.date,
                "user_id": p.user_id,
                "created_at": p.created_at
            } for p in processes
        ]
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
