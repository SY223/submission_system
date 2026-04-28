from pydantic import BaseModel, Field
from fastapi import UploadFile, File, Form
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

    class Config:
        from_attributes = True

class AssignmentListResponse(BaseModel):
    id: UUID
    student_name: str
    subject: str
    subitted_at: datetime

    class Config:
        from_attributes = True

# class AssignmentByStudentResponse(BaseModel):
#     id: UUID
#     subject: str
#     description: Optional[str]
#     submitted_at: datetime

#     class Config:
#         from_attributes = True


# class CommentCreate(BaseModel):
#     teacher_name: str
#     comment: str

#     @classmethod
#     def as_form(
#         cls,
#         teacher_name: str = Form(...),
#         comment: str = Form(...)
#     ):
#         return cls(
#             teacher_name=teacher_name,
#             comment=comment
#         )

# class CommentResponse(BaseModel):
#     id: UUID
#     assignment_id: UUID
#     teacher_id: UUID
#     content: str
#     created_at: datetime

#     class Config:
#         from_attributes = True