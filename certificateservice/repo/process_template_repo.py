from typing import Optional, List

from certificateservice.domain.process_template_schema import ProcessTemplateSchema
from certificateservice.model.process_template_record import ProcessTemplateRecord
from certificateservice.repo.datasource import Repo, DataSource


class ProcessTemplateRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_template(self, template: ProcessTemplateSchema) -> ProcessTemplateRecord:
        # Accept both dict and Pydantic model
        if hasattr(template, "model_dump"):
            data = template.model_dump()
        else:
            data = template
        if hasattr(self.db, "get_session"):
            with self.db.get_session() as sess:
                record = ProcessTemplateRecord(**data)
                sess.add(record)
                sess.commit()
                sess.refresh(record)
                return record
        else:
            record = ProcessTemplateRecord(**data)
            with self.db.get_session() as sess:
                sess.add(record)
                sess.commit()
                sess.refresh(record)
            return record

    def get_templates_by_process(self, user_id: str, process_id: str) -> List[ProcessTemplateRecord]:
        if hasattr(self.db, "get_session"):
            with self.db.get_session() as sess:
                return sess.query(ProcessTemplateRecord).filter(
                    ProcessTemplateRecord.user_id == user_id,
                    ProcessTemplateRecord.process_id == process_id
                ).all()
        else:
            return self.db.query(ProcessTemplateRecord).filter(
                ProcessTemplateRecord.user_id == user_id,
                ProcessTemplateRecord.process_id == process_id
            ).all()

    def get_template_by_id(self, template_id: str) -> Optional[ProcessTemplateRecord]:
        if hasattr(self.db, "get_session"):
            with self.db.get_session() as sess:
                return sess.query(ProcessTemplateRecord).filter(
                    ProcessTemplateRecord.template_id == template_id).first()
        else:
            return self.db.query(ProcessTemplateRecord).filter(ProcessTemplateRecord.template_id == template_id).first()

    def delete_template(self, template_id: str) -> bool:
        if hasattr(self.db, "get_session"):
            with self.db.get_session() as sess:
                record = sess.query(ProcessTemplateRecord).filter(
                    ProcessTemplateRecord.template_id == template_id).first()
                if record:
                    sess.delete(record)
                    sess.commit()
                    return True
                return False
        else:
            record = self.db.query(ProcessTemplateRecord).filter(
                ProcessTemplateRecord.template_id == template_id).first()
            if record:
                self.db.delete(record)
                self.db.commit()
                return True
            return False
