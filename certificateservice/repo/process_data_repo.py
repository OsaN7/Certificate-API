from typing import Optional, List
from certificateservice.model.process_data_record import ProcessDataRecord
from certificateservice.repo.datasource import Repo, DataSource


class ProcessDataRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_process_data(self, process_data: ProcessDataRecord) -> ProcessDataRecord:
        with self.db.get_session() as sess:
            sess.add(process_data)
            sess.commit()
            sess.refresh(process_data)
            return process_data

    def get_process_data_by_user(self, user_id: str) -> List[ProcessDataRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessDataRecord).filter(
                ProcessDataRecord.user_id == user_id
            ).all()

    def get_process_data_by_id(self, process_data_id: str) -> Optional[ProcessDataRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessDataRecord).filter(
                ProcessDataRecord.process_data_id == process_data_id
            ).first()

    def delete_process_data(self, process_data_id: str) -> bool:
        with self.db.get_session() as sess:
            record = sess.query(ProcessDataRecord).filter(
                ProcessDataRecord.process_data_id == process_data_id
            ).first()
            if record:
                sess.delete(record)
                sess.commit()
                return True
            return False
