from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)