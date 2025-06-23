from typing import Optional, List

from pydantic import BaseModel

from certificateservice.domain import BaseResponse
from certificateservice.domain.user import User


class CreateUserRequest(BaseModel):
    user: User
    password: str


class CreateUserResponse(BaseResponse):
    user: Optional[User] = None


class UpdateUserRequest(BaseModel):
    user_id: str
    user: User
    password: Optional[str] = None


class UpdateUserResponse(BaseResponse):
    user: Optional[User] = None


class ListUserRequest(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 10


class ListUserResponse(BaseResponse):
    users: Optional[List[User]] = None


class GetUserRequest(BaseModel):
    user_id: str


class GetUserResponse(BaseResponse):
    error: bool = False
    msg: Optional[str] = None
    user: Optional[User] = None