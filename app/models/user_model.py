import uuid
import enum
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, Enum as SAEnum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_async import Base


if TYPE_CHECKING:
    from app.models.course_model import Course
    from app.models.assignment_model import Assignment
    from app.models.comment_model import Comment


class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, name="user_role"), default=UserRole.student, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    courses: Mapped[List["Course"]] = relationship("Course", back_populates="teacher",lazy="selectin")
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="student", lazy="selectin")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="teacher", lazy="selectin")

    # @property
    # def is_teacher(self) -> bool:
    #     return self.role == UserRole.teacher

    # @property
    # def is_student(self) -> bool:
    #     return self.role == UserRole.student
