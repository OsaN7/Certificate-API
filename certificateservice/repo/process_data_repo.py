from sqlalchemy.orm import Session
from certificateservice.repo.datasource import Repo
from certificateservice.model.process_data_record import ProcessDataRecord


class ProcessDataRepo(Repo):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_data(self, data: dict) -> ProcessDataRecord:
        record = ProcessDataRecord(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_data_by_user(self, user_id: str) -> list[ProcessDataRecord]:
        return self.db.query(ProcessDataRecord).filter(ProcessDataRecord.user_id == user_id).all()
