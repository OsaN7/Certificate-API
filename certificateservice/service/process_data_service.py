import os
import uuid
import shutil
import io
import csv
from certificateservice.model.process_data_record import ProcessDataRecord
from certificateservice.service.email_service import send_email_to_list

class ProcessDataService:
    def __init__(self, db):
        self.db = db

    def add_process_data(self, name, user_id, process_id, csv_file):
        if not process_id:
            process_id = str(uuid.uuid4())
        process_data_id = str(uuid.uuid4())

        file_bytes = csv_file.file.read()
        if not file_bytes:
            raise ValueError("Uploaded CSV file is empty.")

        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        data_dir = os.path.join(base_dir, process_data_id)
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, csv_file.filename)
        with open(csv_path, "wb") as f:
            f.write(file_bytes)

        process_data_record = ProcessDataRecord(
            process_data_id=process_data_id,
            name=name,
            user_id=user_id,
            process_id=process_id,
            # csv_file=file_bytes
            file_path=csv_path

        )
        self.db.add(process_data_record)
        self.db.commit()
        self.db.refresh(process_data_record)

        return {
            "process_data_id": process_data_id,
            "name": name,
            "user_id": user_id,
            "process_id": process_id,
            "csv_file": csv_file.filename
        }

    def list_process_data_urls(self, user_id):
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        urls = []
        for folder in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.lower().endswith('.csv'):
                        url = f"/data/{folder}/{file}"
                        urls.append({"process_data_id": folder, "csv_file": file, "url": url})
        return urls

    def delete_process_data(self, process_data_id):
        data = self.db.query(ProcessDataRecord).filter_by(process_data_id=process_data_id).first()
        if not data:
            raise ValueError("Data not found")

        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        data_dir = os.path.join(base_dir, process_data_id)
        if os.path.isdir(data_dir):
            shutil.rmtree(data_dir)

        self.db.delete(data)
        self.db.commit()
        return {"message": "Data deleted successfully", "data_id": process_data_id}

    async def send_emails_from_csv(self, data, db):
        record = db.query(ProcessDataRecord).filter_by(process_data_id=data.process_data_id).first()
        if not record:
            raise ValueError("Process data not found")


        """If you want to use Binary data to save CSV_File"""
        # csv_bytes = record.csv_file
        # if not csv_bytes:
        #     raise ValueError("No CSV data found in record.")
        # csv_io = io.StringIO(csv_bytes.decode("utf-8"))


        if not record.file_path or not os.path.exists(record.file_path):
            raise ValueError("CSV file not found on disk.")

        with open(record.file_path, "r", encoding="utf-8") as f:
            csv_io = io.StringIO(f.read())
        reader = csv.DictReader(csv_io)
        sent, failed = await send_email_to_list(reader, data.subject, data.body, data.test_email)
        return {
            "test_email_sent_to": data.test_email,
            "emails_sent": sent,
            "emails_failed": failed,
            "total": len(sent) + len(failed)
        } 