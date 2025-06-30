"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/06/2025
"""
from pydantic import BaseModel


class Process(BaseModel):
    process_id: str = None
    name: str = None
    date: str = None  # Date in YYYY-MM-DD format
    user_id: str = None
