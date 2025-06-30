"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/06/2025
"""
from certificateservice.domain.process import Process
from certificateservice.model.process_record import ProcessRecord


def map_process_to_process_record(process: Process) -> ProcessRecord:
    """
    Maps a Process domain object to a ProcessRecord model object.

    :param process: The Process domain object to map.
    :return: A ProcessRecord model object.
    """
    return ProcessRecord(
        process_id=process.process_id,
        name=process.name,
        user_id=process.user_id,
        created_at=process.created_at,
        updated_at=process.updated_at
    )


def map_process_record_to_process(process_record: ProcessRecord) -> Process:
    """
    Maps a ProcessRecord model object to a Process domain object.

    :param process_record:
    :return:
    """

    return Process(
        process_id=process_record.process_id,
        name=process_record.name,
        user_id=process_record.user_id,
    )
