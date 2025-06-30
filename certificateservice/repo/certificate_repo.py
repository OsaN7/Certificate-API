from typing import Optional, List
from typing import List

from certificateservice.domain.certificate import CertificateProcessSchema
from certificateservice.model.certificate_process_record import CertificateProcessRecord
from certificateservice.repo.datasource import Repo, DataSource


class CertificateProcessRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_process(self, process: CertificateProcessSchema) -> CertificateProcessRecord:
        with self.db.get_session() as sess:
            process_record = CertificateProcessRecord(**process.model_dump())
            sess.add(process_record)
            sess.commit()
            sess.refresh(process_record)
            return process_record

    def get_process_by_id(self, process_id: str) -> Optional[CertificateProcessRecord]:
        with self.db.get_session() as sess:
            return sess.query(CertificateProcessRecord).filter(CertificateProcessRecord.process_id == process_id).first()

    def get_processes_by_user(self, user_id: str) -> List[CertificateProcessRecord]:
        with self.db.get_session() as sess:
            return sess.query(CertificateProcessRecord).filter(CertificateProcessRecord.user_id == user_id).all()

    def delete_process(self, process_id: str) -> bool:
        with self.db.get_session() as sess:
            record = sess.query(CertificateProcessRecord).filter(CertificateProcessRecord.process_id == process_id).first()
            if record:
                sess.delete(record)
                sess.commit()
                return True
            return False
