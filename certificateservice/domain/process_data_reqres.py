from typing import Optional, List
from certificateservice.domain.common import BaseRequest, BaseResponse
from certificateservice.domain.process_data_schema import ProcessDataSchema


class AddProcessDataRequest(BaseRequest):
    name: str = None
    user_id: Optional[str] = None
    process_id: Optional[str] = None

class AddProcessDataResponse(BaseResponse):
    # process_data: Optional[ProcessDataSchema] = None
    process_data: None

class ListProcessDataRequest(BaseRequest):
    # user_id: Optional[str] = None
    user_id: None

class ListProcessDataResponse(BaseResponse):
    process_data_list: Optional[List[ProcessDataSchema]] = None

class DeleteProcessDataRequest(BaseRequest):
    process_data_id: Optional[str] = None

class DeleteProcessDataResponse(BaseResponse):
    # success: Optional[bool] = None
    success:  None
