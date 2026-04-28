import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_async import Base

if TYPE_CHECKING:
    from app.models.course_model import Course
    from app.models.user_model import User
    from app.models.comment_model import Comment


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subject: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    course: Mapped["Course"] = relationship("Course", back_populates="assignments", lazy="selectin")
    student: Mapped["User"] = relationship("User", back_populates="assignments", lazy="selectin")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="assignment", lazy="selectin")

    @property
    def student_name(self) -> str:
        if self.student:
            return self.student.full_name
        return "Unknown Student"
