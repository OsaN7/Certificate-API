from certificateservice.domain.common import ErrorCode
from certificateservice.domain.process_reqres import AddProcessRequest, AddProcessResponse, ListProcessesResponse
from certificateservice.mapper.process_mapper import map_process_record_to_process
from certificateservice.model.process_record import ProcessRecord
from certificateservice.repo.process_repo import ProcessRepo
from certificateservice.utils import loggerutil, strutil, uuidutil

logger = loggerutil.get_logger(__name__)


class ProcessService:

    def __init__(self, process_repo: ProcessRepo):
        self.process_repo = process_repo

    def add_certificate_process(self, req: AddProcessRequest) -> AddProcessResponse:
        try:

            if strutil.is_empty(req.name):
                return AddProcessResponse(error=False, error_code=ErrorCode.INVALID_REQUEST, msg="Name cannot be empty")
            if strutil.is_empty(req.user_id):
                return AddProcessResponse(error=False, error_code=ErrorCode.INVALID_REQUEST,
                                          msg="User ID cannot be empty")

            existing_process = self.process_repo.get_process_by_name(req.name, req.user_id)
            if existing_process:
                return AddProcessResponse(error=False, error_code=ErrorCode.CONFLICT,
                                          msg="Process with this name already exists")

            process = ProcessRecord()
            process.process_id = uuidutil.generate_uuid()
            process.name = req.name
            process.user_id = req.user_id

            process = self.process_repo.create_process(process)
            if not process:
                return AddProcessResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR,
                                          msg="Failed to create process")

            p = map_process_record_to_process(process)
            return AddProcessResponse(process=p, )

        except Exception as e:
            logger.error(f"Error adding certificate process: {e}")
            return AddProcessResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))

    def list_process(self, user_id: str) -> ListProcessesResponse:

        try:
            if strutil.is_empty(user_id):
                return ListProcessesResponse(error=False, error_code=ErrorCode.INVALID_REQUEST,
                                             msg="User ID cannot be empty")

            processes = self.process_repo.list_process(user_id)
            if not processes:
                return ListProcessesResponse(error=False, error_code=ErrorCode.NOT_FOUND,
                                             msg="No processes found for this user")

            process_list = [map_process_record_to_process(p) for p in processes]
            return ListProcessesResponse(processes=process_list)

        except Exception as e:
            logger.error(f"Error listing certificate processes: {e}")
            return ListProcessesResponse(error=True, error_code=ErrorCode.INTERNAL_ERROR, msg=str(e))
