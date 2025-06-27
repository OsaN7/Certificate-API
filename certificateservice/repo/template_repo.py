from certificateservice.model.process_template_record import ProcessTemplateRecord
from certificateservice.repo.datasource import Repo, DataSource


class TemplateRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_template(self, template_data: dict) -> ProcessTemplateRecord:
        template = ProcessTemplateRecord(**template_data)
        with self.db.get_session() as session:
            session.add(template)
            session.commit()
            session.refresh(template)

        return template

    def get_templates_by_process(self, user_id: str, process_id: str) -> list[ProcessTemplateRecord]:
        with self.db.get_session() as session:
            return session.query(ProcessTemplateRecord).filter(
                ProcessTemplateRecord.user_id == user_id,
                ProcessTemplateRecord.process_id == process_id
            ).all()
