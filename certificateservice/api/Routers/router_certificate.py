from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from certificateservice.domain.certificate import CertificateRecordSchema
from typing import List

from certificateservice.repo.course_repo import TemplateRepo
from certificateservice.model.course_record import TemplateRecord

from certificateservice.repo.datasource import get_db
# from certificateservice.repo.course_repo import get_all_courses, get_course_by_id
# from certificateservice.domain import CertificateRecordSchema  


router = APIRouter(prefix="/certificates", tags=["Certificates"])

def get_repo(db: Session) -> TemplateRepo:
    return TemplateRepo(db)

@router.get("/{certificate_id}", response_model=CertificateRecordSchema)
def get_certificate(certificate_id: str, db: Session = Depends(get_db)):
    repo = get_repo(db)
    cert = repo.get_course_by_id(certificate_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


@router.get("/", response_model=List[CertificateRecordSchema])
def list_certificates(db: Session = Depends(get_db)):
    repo = get_repo(db)
    return repo.get_all_courses(course_data=None)