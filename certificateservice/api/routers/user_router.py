import traceback

from fastapi import APIRouter, HTTPException

from certificateservice.domain.common import ErrorCode
from certificateservice.domain.user import User
from certificateservice.domain.user_req_res import CreateUserRequest, CreateUserResponse
from certificateservice.repo.datasource import DataSource
from certificateservice.repo.user_repo import UserRepo
from certificateservice.service.user_service import UserService
from certificateservice.utils import loggerutil

router = APIRouter(prefix="/users", tags=["User Management"])

db = DataSource()
user_repo = UserRepo(db=db)
user_service = UserService(user_repo=user_repo)
logger = loggerutil.get_logger(__name__)


@router.post("/signup", response_model=CreateUserResponse)
def signup_user(req: CreateUserRequest):
    try:
        user_record = user_service.create_user(req)
        return CreateUserResponse(
            user=User(
                user_id=user_record.user_id,
                full_name=user_record.full_name,
                username=user_record.username,
                email=user_record.email
            )
        )
    except ValueError as e:
        logger.error(e)
        return CreateUserResponse(error=True, msg=str(e), error_code=ErrorCode.BAD_REQUEST)
    except Exception as e:
        logger.exception(e)
        print("ERROR:", e)
        traceback.print_exc()
        return CreateUserResponse(error=True, msg=str(e), error_code=ErrorCode.BAD_REQUEST)


@router.get("/user_id", response_model=User)
async def get_user(user_id: str):
    try:
        user = user_service.get_user(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user_id", summary="Delete User")
def delete_user(user_id: str):
    try:
        user_service.delete_user(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        logger.error(e)
        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=404, detail=str(e))
