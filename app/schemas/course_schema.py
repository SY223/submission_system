from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
import re
import uuid


class CourseBase(BaseModel):
    title: str
    code: str
    description: Optional[str] = None

    @field_validator("code")
    @classmethod
    def validate_course_code(cls, value: str):
        if not value or not value.strip(): 
            return value
        pattern = r"^[A-Za-z]{3}\d{3}$"
        if not re.match(pattern, value): 
            raise ValueError("Course code not right") 
        return value.upper()  # Normalize to uppercase

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: UUID
    teacher_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

    @field_validator("title", "code", "description") 
    def normalize_fields(cls, value):
        if value is not None:
            return value.strip().lower()
        return value

class CoursePatch(BaseModel):
    title: str | None = None
    code: str | None = None
    description: str | None = None

    @field_validator("title", "code", "description") 
    def normalize_fields(cls, value):
        if value is not None:
            return value.strip().lower()
        return value
    