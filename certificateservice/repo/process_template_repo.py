from typing import Optional, List
from certificateservice.model.process_template_record import ProcessTemplateRecord
from certificateservice.repo.datasource import Repo, DataSource


class ProcessTemplateRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_template(self, template: ProcessTemplateRecord) -> ProcessTemplateRecord:
        with self.db.get_session() as sess:
            sess.add(template)
            sess.commit()
            sess.refresh(template)
            return template

    def get_templates_by_process(self, user_id: str, process_id: str) -> List[ProcessTemplateRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessTemplateRecord).filter(
                ProcessTemplateRecord.user_id == user_id,
                ProcessTemplateRecord.process_id == process_id
            ).all()

    def get_template_by_id(self, template_id: str) -> Optional[ProcessTemplateRecord]:
        with self.db.get_session() as sess:
            return sess.query(ProcessTemplateRecord).filter(
                ProcessTemplateRecord.template_id == template_id
            ).first()

    def delete_template(self, template: ProcessTemplateRecord) -> bool:
        with self.db.get_session() as sess:
            # Attach the instance to the session if needed
            obj = sess.merge(template)
            sess.delete(obj)
            sess.commit()
            return True
