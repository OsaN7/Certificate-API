import os
import shutil
import uuid
from typing import List

from certificateservice.domain.common import ErrorCode
from certificateservice.domain.process_data_reqres import (
    AddProcessDataRequest,
    AddProcessDataResponse,
    ListProcessDataResponse,
    DeleteProcessDataResponse,
)
from certificateservice.mapper.process_data_mapper import map_process_data_record_to_process_data
from certificateservice.model.process_data_record import ProcessDataRecord
from certificateservice.repo.process_data_repo import ProcessDataRepo
from certificateservice.utils import loggerutil, strutil

logger = loggerutil.get_logger(__name__)


class ProcessDataService:
    def __init__(self, process_data_repo: ProcessDataRepo):
        self.process_data_repo = process_data_repo
        self.base_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

    def add_process_data(self, req: AddProcessDataRequest) -> AddProcessDataResponse:
        try:
            if strutil.is_empty(req.name):
                return AddProcessDataResponse(error=True, error_code=ErrorCode.INVALID_REQUEST, msg="Name cannot be empty")
            if strutil.is_empty(req.user_id):
                return AddProcessDataResponse(error=True, error_code=ErrorCode.INVALID_REQUEST, msg="User ID cannot be empty")

            process_id = req.process_id or str(uuid.uuid4())
            process_data_id = str(uuid.uuid4())

            # Read CSV file content
            file_bytes = req.csv_file.file.read()
            if not file_bytes:
                return AddProcessDataResponse(error=True, error_code=ErrorCode.INVALID_REQUEST, msg="Uploaded CSV file is empty.")

            # Create directory for storing CSV file
            data_dir = os.path.join(self.base_data_dir, process_data_id)
            os.makedirs(data_dir, exist_ok=True)

            csv_path = os.path.join(data_dir, req.csv_file.filename)
            with open(csv_path, "wb") as f:
                f.write(file_bytes)

            record = ProcessDataRecord(
                process_data_id=process_data_id,
                name=req.name,
                user_id=req.user_id,
                process_id=process_id,
                file_path=csv_path,
            )

            saved_record = self.process_data_repo.create_process_data(record)
            process_data = map_process_data_record_to_process_data(saved_record)

            return AddProcessDataResponse(process_data=process_data)

        except Exception as e:
            logger.error(f"Error adding process data: {e}")
            return AddProcessDataResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    def list_process_data(self, user_id: str) -> ListProcessDataResponse:
        try:
            if strutil.is_empty(user_id):
                return ListProcessDataResponse(error=True, error_code=ErrorCode.INVALID_REQUEST, msg="User ID cannot be empty")

            records: List[ProcessDataRecord] = self.process_data_repo.get_process_data_by_user(user_id)
            if not records:
                return ListProcessDataResponse(error=True, error_code=ErrorCode.NOT_FOUND, msg="No process data found for this user")

            process_data_list = [map_process_data_record_to_process_data(rec) for rec in records]

            return ListProcessDataResponse(process_data_list=process_data_list)

        except Exception as e:
            logger.error(f"Error listing process data: {e}")
            return ListProcessDataResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    def delete_process_data(self, process_data_id: str) -> DeleteProcessDataResponse:
        try:
            record = self.process_data_repo.get_process_data_by_id(process_data_id)
            if not record:
                return DeleteProcessDataResponse(error=True, error_code=ErrorCode.NOT_FOUND, msg="Process data not found")

            # Remove directory and files on disk
            data_dir = os.path.join(self.base_data_dir, process_data_id)
            if os.path.isdir(data_dir):
                shutil.rmtree(data_dir)

            deleted = self.process_data_repo.delete_process_data(process_data_id)
            if deleted:
                return DeleteProcessDataResponse(msg="Process data deleted successfully", process_data_id=process_data_id)
            else:
                return DeleteProcessDataResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg="Failed to delete process data")

        except Exception as e:
            logger.error(f"Error deleting process data: {e}")
            return DeleteProcessDataResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    async def send_emails_from_csv(self, data, db):
        try:
            record = self.process_data_repo.get_process_data_by_id(data.process_data_id)
            if not record:
                raise ValueError("Process data not found")

            if not record.file_path or not os.path.exists(record.file_path):
                raise ValueError("CSV file not found on disk.")

            import csv
            import io

            with open(record.file_path, "r", encoding="utf-8") as f:
                csv_io = io.StringIO(f.read())

            reader = csv.DictReader(csv_io)

            # Implement your email sending logic here (async)
            # Example:
            # sent, failed = await send_email_to_list(reader, data.subject, data.body, data.test_email)
            # return {
            #     "test_email_sent_to": data.test_email,
            #     "emails_sent": sent,
            #     "emails_failed": failed,
            #     "total": len(sent) + len(failed)
            # }

            return {"message": "send_emails_from_csv method not yet implemented"}

        except Exception as e:
            logger.error(f"Error sending emails from CSV: {e}")
            raise
