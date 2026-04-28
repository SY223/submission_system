from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"

class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: UUID
    role: UserRole
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class UserPatch(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None

