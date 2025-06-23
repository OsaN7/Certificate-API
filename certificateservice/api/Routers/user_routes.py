from fastapi import APIRouter, HTTPException, Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession
from certificateservice.domain.user import User
from certificateservice.repo.datasource import DataSource, get_db  

from certificateservice.model.user_record import UserRecord  
from certificateservice.domain.common import ErrorCode

from certificateservice.repo.user_repo import UserRepo
from certificateservice.service import user_service
from certificateservice.utils import loggerutil
from certificateservice.domain.user_req_res import CreateUserRequest


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db = DataSource()
user_repo = UserRepo(db=db)
# auth_service = AuthService(user_repo=user_repo)
user_service = user_service.UserService(user_repo=user_repo)
logger = loggerutil.get_logger(__name__)
logger=loggerutil.get_logger(__name__)

@router.post("/signup", response_model=User)
def signup_user(req: CreateUserRequest):
    try:
        user_record = user_service.create_user(req)
        return User(
            user_id=user_record.user_id,
            full_name=user_record.full_name,
            username=user_record.username,
            email=user_record.email
        )
    except ValueError as e:
        logger.error(e)
        return User(error=True, msg=str(e), code=ErrorCode.BAD_REQUEST)
    except Exception as e:
        logger.exception(e)
        return User(error=True, msg=str(e), code=ErrorCode.INTERNAL_ERROR)
    


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
   
    user = await db.get(UserRecord, user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
