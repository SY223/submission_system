import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_async import Base

if TYPE_CHECKING:
    from app.models.assignment_model import Assignment
    from app.models.user_model import User

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assignment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
    teacher_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    assignment: Mapped["Assignment"] = relationship("Assignment", back_populates="comments", lazy="selectin")
    teacher: Mapped["User"] = relationship("User",back_populates="comments",lazy="selectin")
