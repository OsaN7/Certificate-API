from typing import Optional, List

from certificateservice.domain.process_data_schema import ProcessDataSchema
from certificateservice.model.process_data_record import ProcessRecord
from certificateservice.repo.datasource import Repo, DataSource


class ProcessDataRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_data(self, data: ProcessDataSchema) -> ProcessRecord:
        with self.db.get_session() as sess:
            record = ProcessRecord(**data.model_dump())
            sess.add(record)
            sess.commit()
            sess.refresh(record)
            return record

    def get_data_by_id(self, process_data_id: str) -> Optional[ProcessRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessRecord).filter(
                ProcessRecord.process_data_id == process_data_id
            ).first()

    def get_data_by_user(self, user_id: str) -> List[ProcessRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessRecord).filter(
                ProcessRecord.user_id == user_id
            ).all()

    def delete_data(self, process_data_id: str) -> bool:
        with self.db.get_session() as sess:
            record = sess.query(ProcessRecord).filter(
                ProcessRecord.process_data_id == process_data_id
            ).first()
            if record:
                sess.delete(record)
                sess.commit()
                return True
            return False
