from certificateservice.domain.user_req_res import CreateUserRequest
from certificateservice.repo.user_repo import UserRepo
from certificateservice.utils.exception import InvalidError


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def create_user(self, request: CreateUserRequest):
        if self.user_repo.get_by_email(request.user.email):
            raise InvalidError("User already exists with this email.")
        user_dict = request.user.dict()
        user = self.user_repo.create_user(user_dict, request.password)
        return user

    def get_user(self, email: str):
        user = self.user_repo.get_by_email(email)
        if not user:
            raise InvalidError("User not found.")
        return user

    def delete_user(self, user_id: str):
        success = self.user_repo.delete_user(user_id)
        if not success:
            raise InvalidError("User not found.")
        return success
