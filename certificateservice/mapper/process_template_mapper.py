"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 01/07/2025
"""

from certificateservice.domain.process_template_schema import ProcessTemplateSchema
from certificateservice.model.process_template_record import ProcessTemplateRecord
import base64


def map_template_record_to_domain(template: ProcessTemplateSchema) -> ProcessTemplateRecord:
    """
    Maps a ProcessTemplateSchema domain object to a ProcessTemplateSchema model object.

    :param template: The ProcessTemplateSchema domain object to map.
    :return: A ProcessTemplateRecord model object.
    """
    return ProcessTemplateRecord(
        template_id=template.template_id,
        name=template.name,
        user_id=template.user_id,
        process_id=template.process_id,
        template_file=template.template_file,
        created_at=template.created_at
    )


def map_template_record_to_template(template_record: ProcessTemplateRecord) -> ProcessTemplateSchema:
    """
    Maps a ProcessTemplateRecord model object to a ProcessTemplateSchema domain object.

    :param template_record: The ProcessTemplateRecord model object to map.
    :return: A ProcessTemplateSchema domain object.
    """
    return ProcessTemplateSchema(
        template_id=template_record.template_id,
        name=template_record.name,
        user_id=template_record.user_id,
        process_id=template_record.process_id,
        template_file=base64.b64encode(template_record.template_file).decode('utf-8') if template_record.template_file else None,
        created_at=template_record.created_at
    )


