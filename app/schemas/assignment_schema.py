from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class AssignmentCreate(BaseModel):
    student_name: str
    subject: str
    description: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: UUID
    course_id: UUID
    student_id: UUID
    student_name: str
    subject: str
    description: Optional[str]
    file_path: str
    original_filename: str
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AssignmentListResponse(BaseModel):
    id: UUID
    student_name: str
    subject: str
    subitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

