from typing import List
from typing import Optional

from certificateservice.model.process_record import ProcessRecord
from certificateservice.repo.datasource import Repo, DataSource


class ProcessRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_process(self, process: ProcessRecord) -> ProcessRecord:
        with self.db.get_session() as sess:
            sess.add(process)
            sess.commit()
            sess.refresh(process)
            return process

    def get_process_by_id(self, process_id: str) -> Optional[ProcessRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessRecord).filter(
                ProcessRecord.process_id == process_id).first()

    def get_processes_by_user(self, user_id: str) -> List[ProcessRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessRecord).filter(ProcessRecord.user_id == user_id).all()

    def delete_process(self, process_id: str) -> bool:
        with self.db.get_session() as sess:
            record = sess.query(ProcessRecord).filter(
                ProcessRecord.process_id == process_id).first()
            if record:
                sess.delete(record)
                sess.commit()
                return True
            return False

    def get_process_by_name(self, name, user_id: str):
        with self.db.get_session() as sess:
            return sess.query(ProcessRecord).filter(
                ProcessRecord.name == name, ProcessRecord.user_id == user_id).first()

    def list_process(self, user_id):
        with self.db.get_session() as sess:
            return sess.query(ProcessRecord).filter(
                ProcessRecord.user_id == user_id).all()
