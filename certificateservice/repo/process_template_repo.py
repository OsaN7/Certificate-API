from sqlalchemy.orm import Session
from certificateservice.repo.datasource import  Repo
from certificateservice.model.process_template_record import ProcessTemplateRecord

class ProcessTemplateRepo(Repo):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_template(self, template_data: dict) -> ProcessTemplateRecord:
        template = ProcessTemplateRecord(**template_data)
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def get_templates_by_process(self, user_id: str, process_id: str) -> list[ProcessTemplateRecord]:
        return self.db.query(ProcessTemplateRecord).filter(
            ProcessTemplateRecord.user_id == user_id,
            ProcessTemplateRecord.process_id == process_id
        ).all()
