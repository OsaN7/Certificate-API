import os
import shutil
import traceback
import uuid

from certificateservice.repo.process_template_repo import ProcessTemplateRepo
from fastapi import APIRouter, Depends, HTTPException, Body, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from certificateservice.model.process_template_record import ProcessTemplateRecord
from certificateservice.repo.datasource import get_db

router = APIRouter(prefix="/certificates/process")


@router.post("/process/template", tags=["Process Template Page"], summary="Add Process Template")
def add_process_template(
        name: str = Body(..., description="Template name"),
        user_id: str = Body(..., description="User ID"),
        process_id: str = Body(None, description="Process ID (optional, will be generated if not provided)"),
        template_file: UploadFile = File(..., description="Template file (PDF)"),
        db: Session = Depends(get_db)
):
    """Add a template to a certificate process. If process_id is not provided, a new one will be generated. Stores the actual PDF file in the database and in data/{template_id}/ (no metadata.json)."""
    try:
        if not process_id:
            process_id = str(uuid.uuid4())
        template_id = str(uuid.uuid4())
        file_bytes = template_file.file.read()
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        template_dir = os.path.join(base_dir, template_id)
        os.makedirs(template_dir, exist_ok=True)
        pdf_path = os.path.join(template_dir, template_file.filename)
        with open(pdf_path, "wb") as f:
            f.write(file_bytes)
        repo = ProcessTemplateRepo(db)
        template = repo.create_template({
            "template_id": template_id,
            "name": name,
            "user_id": user_id,
            "process_id": process_id,
            "template_file": file_bytes
        })
        return {
            "template_id": template.template_id,
            "name": template.name,
            "user_id": template.user_id,
            "process_id": template.process_id,
            "created_at": template.created_at
        }
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/templates", tags=["Process Template Page"], summary="List Process Templates")
def list_process_templates(
        user_id: str = Query(..., description="User ID"),
        process_id: str = Query(..., description="Process ID"),
        db: Session = Depends(get_db)
):
    try:
        repo = ProcessTemplateRepo(db)
        templates = repo.get_templates_by_process(user_id, process_id)
        return [
            {
                "template_id": t.template_id,
                "name": t.name,
                "user_id": t.user_id,
                "process_id": t.process_id,
                "created_at": t.created_at
            }
            for t in templates
        ]
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/template/download", tags=["Process Template Page"], summary="Download Process Template PDF")
def download_process_template(template_id: str = Query(..., description="Template ID"), db: Session = Depends(get_db)):
    try:
        template = db.query(ProcessTemplateRecord).filter_by(template_id=template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        return StreamingResponse(
            iter([template.template_file]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={template_id}.pdf"}
        )
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/process/template", tags=["Process Template Page"], summary="Delete Process Template")
def delete_process_template(template_id: str = Query(..., description="Template ID"), db: Session = Depends(get_db)):
    try:
        template = db.query(ProcessTemplateRecord).filter_by(template_id=template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        # Remove the template's folder from disk (data/{template_id})
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        template_dir = os.path.join(base_dir, template_id)
        if os.path.isdir(template_dir):
            shutil.rmtree(template_dir)
        db.delete(template)
        db.commit()
        return {"message": "Template deleted successfully", "template_id": template_id}
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/process/template/test-url", tags=["Process Template Page"], summary="Test Template URL")
def test_template_url(template_id: str = Query(..., description="Template ID")):
    try:
        url = f"/certificates/process/template/download?template_id={template_id}"
        return {"url": url}
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
