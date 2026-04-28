from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CommentCreate(BaseModel):
    teacher_name: str
    comment: str


class CommentResponse(BaseModel):
    id: UUID
    assignment_id: UUID
    teacher_id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True