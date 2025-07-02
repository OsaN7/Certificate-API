"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Updated on: 02/07/2025
"""

from typing import Optional, List
from certificateservice.domain.common import BaseRequest, BaseResponse
from certificateservice.domain.process import Process


class AddProcessRequest(BaseRequest):
    name: Optional[str] = None
    date: Optional[str] = None
    user_id: Optional[str] = None


class AddProcessResponse(BaseResponse):
    process: Optional[Process] = None


class ListProcessesRequest(BaseRequest):
    user_id: Optional[str] = None


class ListProcessesResponse(BaseResponse):
    processes: Optional[List[Process]] = None
