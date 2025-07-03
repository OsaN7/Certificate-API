from typing import Optional, List
from sqlalchemy.orm import Session 
from certificateservice.model.process_data_record import ProcessDataRecord


class ProcessDataRepo:
    def __init__(self, db: Session):  
        self.db = db

    def create_process_data(self, process_data: ProcessDataRecord) -> ProcessDataRecord:
        self.db.add(process_data)
        self.db.commit()
        self.db.refresh(process_data)
        return process_data

    def get_process_data_by_user(self, user_id: str) -> List[ProcessDataRecord]:
        return self.db.query(ProcessDataRecord).filter(
            ProcessDataRecord.user_id == user_id
        ).all()

    def get_process_data_by_id(self, process_data_id: str) -> Optional[ProcessDataRecord]:
        return self.db.query(ProcessDataRecord).filter(
            ProcessDataRecord.process_data_id == process_data_id
        ).first()

    def delete_process_data(self, process_data_id: str) -> bool:
        record = self.db.query(ProcessDataRecord).filter(
            ProcessDataRecord.process_data_id == process_data_id
        ).first()
        if record:
            self.db.delete(record)
            self.db.commit()
            return True
        return False
