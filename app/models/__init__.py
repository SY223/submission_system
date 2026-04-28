from app.core.db import Base

# Import all models here so Alembic + SQLAlchemy can see them
from app.models.user_model import User
from app.models.course_model import Course
from app.models.assignment_model import Assignment
from app.models.comment_model import Comment

__all__ = ["User", "Course", "Assignment", "Comment"]