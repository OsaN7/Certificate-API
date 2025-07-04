import os
import shutil
import uuid
import base64
from fastapi.responses import StreamingResponse

from certificateservice.domain.common import ErrorCode
from certificateservice.domain.process_template_reqres import (
    AddTemplateRequest,
    AddTemplateResponse,
    ListTemplateResponse,
    DeleteTemplateResponse
)
from certificateservice.mapper.process_template_mapper import map_template_record_to_template
from certificateservice.model.process_template_record import ProcessTemplateRecord
from certificateservice.repo.process_template_repo import ProcessTemplateRepo
from certificateservice.utils import loggerutil, strutil

logger = loggerutil.get_logger(__name__)


class ProcessTemplateService:

    def __init__(self, repo: ProcessTemplateRepo):
        self.repo = repo

    def add_process_template(self, req: AddTemplateRequest) -> AddTemplateResponse:
        try:
            if strutil.is_empty(req.name):
                return AddTemplateResponse(error=True, error_code=ErrorCode.INVALID_REQUEST, msg="Template name is required")
            if strutil.is_empty(req.user_id):
                return AddTemplateResponse(error=True, error_code=ErrorCode.INVALID_REQUEST, msg="User ID is required")

            process_id = req.process_id or str(uuid.uuid4())
            template_id = str(uuid.uuid4())

            record = ProcessTemplateRecord()
            record.template_id = template_id
            record.name = req.name
            record.user_id = req.user_id
            record.process_id = process_id
            record.template_file = None  # No file saved yet

            saved_record = self.repo.create_template(record)
            if not saved_record:
                return AddTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg="Failed to save template metadata")

            template = map_template_record_to_template(saved_record)
            # No file to encode yet
            template.template_file = None
            return AddTemplateResponse(template=template)

        except Exception as e:
            logger.error(f"Error adding process template metadata: {e}")
            return AddTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))


    # Step 2: Upload file separately
    def upload_process_template_file(self, template_id: str, template_file) -> AddTemplateResponse:
        try:
            template_record = self.repo.get_template_by_id(template_id)
            if not template_record:
                return AddTemplateResponse(error=True, error_code=ErrorCode.NOT_FOUND, msg="Template metadata not found")

            file_bytes = template_file.file.read()

            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
            template_dir = os.path.join(base_dir, template_id)
            os.makedirs(template_dir, exist_ok=True)

            pdf_path = os.path.join(template_dir, template_file.filename)
            with open(pdf_path, "wb") as f:
                f.write(file_bytes)

            # Update the existing record with the file bytes
            template_record.template_file = file_bytes

            saved_record = self.repo.update_template(template_record)
            if not saved_record:
                return AddTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg="Failed to save template file")

            template = map_template_record_to_template(saved_record)
            if template.template_file is not None:
                template.template_file = base64.b64encode(saved_record.template_file).decode('utf-8')
            return AddTemplateResponse(template=template)

        except Exception as e:
            logger.error(f"Error uploading process template file: {e}")
            return AddTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    def list_process_templates(self, user_id: str, process_id: str) -> ListTemplateResponse:
        try:
            if strutil.is_empty(user_id) or strutil.is_empty(process_id):
                return ListTemplateResponse(error=True, error_code=ErrorCode.INVALID_REQUEST, msg="User ID and Process ID are required")

            templates = self.repo.get_templates_by_process(user_id, process_id)
            if not templates:
                return ListTemplateResponse(error=False, error_code=ErrorCode.NOT_FOUND, msg="No templates found")

            template_list = []
            for t in templates:
                template = map_template_record_to_template(t)
                if template.template_file is not None:
                    template.template_file = base64.b64encode(t.template_file).decode('utf-8')
                template_list.append(template)
            return ListTemplateResponse(templates=template_list)

        except Exception as e:
            logger.error(f"Error listing process templates: {e}")
            return ListTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    def download_process_template(self, template_id: str):
        try:
            template = self.repo.get_template_by_id(template_id)
            if not template:
                return None

            return StreamingResponse(
                iter([template.template_file]),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={template_id}.pdf"}
            )

        except Exception as e:
            logger.error(f"Error downloading template: {e}")
            return None

    def delete_process_template(self, template_id: str) -> DeleteTemplateResponse:
        try:
            template = self.repo.get_template_by_id(template_id)
            if not template:
                return DeleteTemplateResponse(error=True, error_code=ErrorCode.NOT_FOUND, msg="Template not found")

            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
            template_dir = os.path.join(base_dir, template_id)
            if os.path.isdir(template_dir):
                shutil.rmtree(template_dir)

            # Correct: delete using the instance
            self.repo.delete_template(template)

            return DeleteTemplateResponse(success=True, msg="Template deleted successfully")

        except Exception as e:
            logger.error(f"Error deleting template: {e}")
            return DeleteTemplateResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    def test_template_url(self, template_id: str):
        try:
            url = f"/certificates/process-template/download?template_id={template_id}"
            return {"url": url}
        except Exception as e:
            logger.error(f"Error generating test URL: {e}")
            return {"error": True, "error_code": ErrorCode.INTERNAL_ERROR, "msg": str(e)}
