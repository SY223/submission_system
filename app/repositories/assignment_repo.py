from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.assignment_model import Assignment
from uuid import UUID
import uuid



class AssignmentRepository:
    @staticmethod
    async def create_assignment(
        db: AsyncSession,
        data: dict
    ):
        new_assignment = Assignment(**data)
        db.add(new_assignment)
        await db.flush()
        await db.refresh(new_assignment)
        return new_assignment
    
    @staticmethod
    async def get_assignment_by_id(
        db: AsyncSession,
        assignment_id: uuid.UUID
    ):
        result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_assignments_by_student_name(db: AsyncSession, student_name: str):
        result = await db.execute(
            select(Assignment).where(
                Assignment.student.has(full_name=student_name)
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_all_assignments(db: AsyncSession):
        result = await db.execute(select(Assignment))
        return result.scalars().all()
    
    @staticmethod
    async def get_assignments_by_student_id(db: AsyncSession, student_id: UUID):
        result = await db.execute(
            select(Assignment).where(Assignment.student_id == student_id)
        )
        return result.scalars().all()

    @staticmethod
    async def student_has_submitted(
        db: AsyncSession,
        student_id: UUID,
        course_id: UUID
    ):
        result = await db.execute(
            select(Assignment).where(
                Assignment.student_id == student_id,
                Assignment.course_id == course_id
            )
        )
        return result.scalars().first()

    


    

    