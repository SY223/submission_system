from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.comment_repo import CommentRepository
from app.repositories.assignment_repo import AssignmentRepository
from app.repositories.user_repo import UserRepository
from app.schemas.comment_schema import CommentCreate, CommentResponse
from uuid import UUID



class CommentService:
    @staticmethod
    async def add_comment(
        db: AsyncSession,
        assignment_id: UUID,
        data: CommentCreate
    ):
        teacher_name = data.teacher_name.strip()
        teacher = await UserRepository.get_user_by_full_name(db, teacher_name)
        if not teacher:
              raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found"
            )
        if teacher.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only teachers can comment on assignments"
            )
        assignment = await AssignmentRepository.get_assignment_by_id(db, assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        #Prepare submission
        comment_dict = {
            "assignment_id": assignment.id,
            "teacher_id": teacher.id,
            "content": data.content
        }
        comment = await CommentRepository.create_comment(db, comment_dict)
        return comment

        