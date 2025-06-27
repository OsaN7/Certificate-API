from certificateservice.model.certificate_process_record import CertificateProcessRecord
from certificateservice.repo.datasource import Repo, DataSource


class CertificateProcessRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def create_process(self, process_data: dict) -> CertificateProcessRecord:
        process = CertificateProcessRecord(**process_data)
        with self.db.get_session() as session:
            session.add(process)
            session.commit()
            session.refresh(process)

        return process

    def get_processes_by_user(self, user_id: str) -> list[CertificateProcessRecord]:
        with self.db.get_session() as session:
            return session.query(CertificateProcessRecord).filter(CertificateProcessRecord.user_id == user_id).all()

# class TemplateRepo(Repo):
#     def __init__(self, db: DataSource):
#         super().__init__(db)

#     def get_course_by_id(self, id: str) -> TemplateRecord | None:
#         with self.db.get_session() as sess:
#             return sess.query(TemplateRecord).filter(TemplateRecord.id == id).first()

#     def get_all_courses(self,course_data) -> list[TemplateRecord]:
#         with self.db.get_session() as sess:
#             return self.query(TemplateRecord).all()

#     def create_course(self, course_data: dict) -> TemplateRecord:
#         with self.db.get_session() as sess:
#             course = TemplateRecord(**course_data)
#             sess.add(course)
#             sess.commit()
#             sess.refresh(course)
#             return course

#     def update_course(self, course_id: str, course_data: dict) -> TemplateRecord | None:
#         with self.db.get_session() as sess:
#             # course = sess.get_course_by_id(sess, course_id)
#             course = sess.query(TemplateRecord).filter(TemplateRecord.id == course_id).first()
#             if not course:
#                 return None
#             for key, value in course_data.items():
#                 setattr(course, key, value)
#             sess.commit()
#             sess.refresh(course)
#             return course
