import os
import uuid
import shutil
from fastapi.responses import StreamingResponse
from certificateservice.repo.process_template_repo import ProcessTemplateRepo
from certificateservice.model.process_template_record import ProcessTemplateRecord

class ProcessTemplateService:
    def __init__(self, repo: ProcessTemplateRepo, db):
        self.repo = repo
        self.db = db

    def add_process_template(self, name, user_id, process_id, template_file):
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
        template = self.repo.create_template({
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

    def list_process_templates(self, user_id, process_id):
        templates = self.repo.get_templates_by_process(user_id, process_id)
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

    def download_process_template(self, template_id):
        template = self.db.query(ProcessTemplateRecord).filter_by(template_id=template_id).first()
        if not template:
            return None
        return StreamingResponse(
            iter([template.template_file]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={template_id}.pdf"}
        )

    def delete_process_template(self, template_id):
        template = self.db.query(ProcessTemplateRecord).filter_by(template_id=template_id).first()
        if not template:
            return None
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        template_dir = os.path.join(base_dir, template_id)
        if os.path.isdir(template_dir):
            shutil.rmtree(template_dir)
        self.db.delete(template)
        self.db.commit()
        return {"message": "Template deleted successfully", "template_id": template_id}

    def test_template_url(self, template_id):
        url = f"/certificates/process/template/download?template_id={template_id}"
        return {"url": url} 