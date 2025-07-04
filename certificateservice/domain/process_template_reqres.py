from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from certificateservice.domain.common import BaseRequest, BaseResponse
from certificateservice.domain.process_template_schema import ProcessTemplateSchema


class AddTemplateRequest(BaseRequest):
    name: Optional[str] = None
    user_id: Optional[str] = None
    process_id: Optional[str] = None


class AddTemplateResponse(BaseResponse):
    template: ProcessTemplateSchema = None  

class AddTemplateEntity(BaseModel):
    name: str
    user_id: str
    process_id: Optional[str] = None
    template_file: UploadFile

class ListTemplatesRequest(BaseRequest):
    user_id: str = None
    process_id: str = None


class ListTemplateResponse(BaseResponse):
    templates: list[ProcessTemplateSchema] = None  


class DeleteTemplateRequest(BaseRequest):
    template_id: str = None


class DeleteTemplateResponse(BaseResponse):
    success: bool = False
