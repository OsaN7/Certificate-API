from certificateservice.model.process_data_record import ProcessDataRecord
from certificateservice.repo.datasource import Repo, DataSource


class ProcessDataRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_data(self, data: dict) -> ProcessDataRecord:
        record = ProcessDataRecord(**data)
        with self.db.get_session() as session:
            session.add(record)
            session.commit()
            session.refresh(record)
        return record

    def get_data_by_user(self, user_id: str) -> list[ProcessDataRecord]:
        with self.db.get_session() as session:
            return session.query(ProcessDataRecord).filter(ProcessDataRecord.user_id == user_id).all()
