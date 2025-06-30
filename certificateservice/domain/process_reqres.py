"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/06/2025
"""
from certificateservice.domain.common import BaseRequest, BaseResponse
from certificateservice.domain.process import Process


class AddProcessRequest(BaseRequest):
    name: str = None
    date: str = None
    user_id: str = None


class AddProcessResponse(BaseResponse):
    process: Process = None


class ListProcessesRequest(BaseRequest):
    user_id: str = None


class ListProcessesResponse(BaseResponse):
    processes: list[Process] = None
