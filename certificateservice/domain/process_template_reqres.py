from certificateservice.domain.common import BaseRequest, BaseResponse
from certificateservice.domain.process_template_schema import ProcessTemplateSchema


class AddTemplateRequest(BaseRequest):
    name: str = None
    user_id: str = None
    process_id: str = None


class AddTemplateResponse(BaseResponse):
    template: ProcessTemplateSchema = None  


class ListTemplatesRequest(BaseRequest):
    user_id: str = None
    process_id: str = None


class ListTemplateResponse(BaseResponse):
    templates: list[ProcessTemplateSchema] = None  


class DeleteTemplateRequest(BaseRequest):
    template_id: str = None


class DeleteTemplateResponse(BaseResponse):
    success: bool = False
