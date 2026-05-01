from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.course_model import Course
from uuid import UUID


class CourseRepository:
    @staticmethod
    async def create_course(db: AsyncSession, data: dict):
        new_course = Course(
            title=data["title"],
            code=data["code"],
            description=data.get("description"),
            teacher_id=data["teacher_id"]
        )
        db.add(new_course)
        await db.flush()
        await db.refresh(new_course)
        return new_course

    @staticmethod
    async def get_course_by_code(db: AsyncSession, course_code):
        result = await db.execute(select(Course).where(Course.code == course_code))
        return result.scalars().first()

    @staticmethod
    async def get_course_by_id(db: AsyncSession, course_id: UUID):
        result = await db.execute(select(Course).where(Course.id == course_id))
        return result.scalars().first()

    @staticmethod
    async def get_all_courses(db: AsyncSession):
        result = await db.execute(select(Course))
        return result.scalars().all()

    @staticmethod
    async def update_course(
        db: AsyncSession,
        course: Course,
        data: dict
    ):
        for field, value in data.items():
            setattr(course, field, value)
        await db.flush()
        await db.refresh(course)
        return course

    @staticmethod
    async def delete_course(db: AsyncSession, course: Course):
        await db.delete(course)
        await db.flush()
