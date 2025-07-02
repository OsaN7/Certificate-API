"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 01/07/2025
"""

from certificateservice.domain.process_data_schema import ProcessDataSchema
from certificateservice.model.process_data_record import ProcessDataRecord


def map_process_data_to_process_data_record(process_data: ProcessDataSchema) -> ProcessDataRecord:
    """
    Maps a ProcessDataSchema domain object to a ProcessDataRecord model object.

    :param process_data: The ProcessDataSchema domain object to map.
    :return: A ProcessDataRecord model object.
    """
    return ProcessDataRecord(
        process_data_id=process_data.process_data_id,
        name=process_data.name,
        user_id=process_data.user_id,
        process_id=process_data.process_id,
        file_path=getattr(process_data, 'file_path', None),  # Optional handling if domain has it
        created_at=process_data.created_at
    )


def map_process_data_record_to_process_data(process_data_record: ProcessDataRecord) -> ProcessDataSchema:
    """
    Maps a ProcessDataRecord model object to a ProcessDataSchema domain object.

    :param process_data_record: The ProcessDataRecord model object to map.
    :return: A ProcessDataSchema domain object.
    """
    return ProcessDataSchema(
        process_data_id=process_data_record.process_data_id,
        name=process_data_record.name,
        user_id=process_data_record.user_id,
        process_id=process_data_record.process_id,
        # file_path is omitted if domain doesn't have it
        created_at=process_data_record.created_at
    )
