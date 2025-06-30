from certificateservice.domain.certificate import CertificateProcessSchema
from certificateservice.repo.certificate_repo import CertificateProcessRepo
import os
import json
from datetime import datetime
import uuid

class CertificateService:

    def __init__(self, repo=None):
        self.repo = repo or CertificateProcessRepo()

    def add_certificate_process(self, name, date, user_id):
        # Generate process_id
        process_id = str(uuid.uuid4())

        # Create directory for certificate process
        process_dir = os.path.join("certificates", process_id)
        os.makedirs(process_dir, exist_ok=True)

        metadata = {
            "name": name,
            "date": date,
            "user_id": user_id,
            "process_id": process_id
        }
        with open(os.path.join(process_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f)

        # ]Create Pydantic schema instance with explicit created_at
        process_schema = CertificateProcessSchema(
            process_id=process_id,
            name=name,
            date=date,
            user_id=user_id,
            created_at=datetime.utcnow()  
        )

        # Save to DB
        self.repo.create_process(process_schema)
        return {"message": "Certificate process added successfully", "process_id": process_id}
