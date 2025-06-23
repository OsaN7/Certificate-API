from sqlalchemy.orm import Session
from typing import Optional
from certificateservice.model.user_record import UserRecord
from certificateservice.repo.datasource import DataSource, Repo


class UserRepo(Repo):
    def __init__(self, db:DataSource):
        super().__init__(db)
    
    
    def get_user_by_id(self,  user_id: str) -> Optional[UserRecord]:
        with self.db.get_session() as sess:
            return sess.query(UserRecord).filter(UserRecord.user_id == user_id).first()

    def get_all_users(self) -> list[UserRecord]:
        with self.db.get_session() as sess:
            return sess.query(UserRecord).all()

    def create_user(self, user: dict, password: str) -> UserRecord:
        with self.db.get_session() as sess:
            user_record = UserRecord(**user, password=password)
            sess.add(user_record)
            sess.commit()
            sess.refresh(user_record)
            return user_record

    def get_by_email(self, email: str) -> Optional[UserRecord]:
        with self.db.get_session() as session:
            return session.query(UserRecord).filter(UserRecord.email == email).first()




