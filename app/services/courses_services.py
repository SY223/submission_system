from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.course_schema import (
    CourseCreate, CourseResponse, CourseUpdate, CoursePatch
)
from app.repositories.course_repo import CourseRepository
from app.models.user_model import UserRole
from app.models.user_model import User
from uuid import UUID


class CourseService:
    @staticmethod
    async def create_course(db: AsyncSession, data: CourseCreate, current_user: User):
        if current_user.role != UserRole.teacher:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only teachers can create courses"
            )

        existing = await CourseRepository.get_course_by_code(db, data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A course with this code already exists"
            )
        course_dict = data.model_dump()
        course_dict["teacher_id"] = current_user.id
        course = await CourseRepository.create_course(db, course_dict)
        await db.commit()
        await db.refresh(course)
        return CourseResponse.model_validate(course)

    @staticmethod
    async def get_all_courses(db: AsyncSession):
        courses = await CourseRepository.get_all_courses(db)
        if not courses:
            raise HTTPException(status_code=404, detail="No course in library")
        return [CourseResponse.model_validate(c) for c in courses]

    @staticmethod
    async def get_course_by_code(db: AsyncSession, course_code: str):
        normalised_code = course_code.strip().upper()
        course = await CourseRepository.get_course_by_code(db, normalised_code)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return CourseResponse.model_validate(course)

    @staticmethod
    async def get_course_by_id(db: AsyncSession, course_id: UUID):
        course = await CourseRepository.get_course_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return CourseResponse.model_validate(course)

    @staticmethod
    async def update_course(
        db: AsyncSession,
        course_id: UUID,
        data: CourseUpdate,
        current_user
    ):
        if current_user.role != UserRole.teacher:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can update courses")
        #
        course = await CourseRepository.get_course_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        if course.teacher_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to modify this course")
        update_dict = data.model_dump(exclude_unset=False)

        if update_dict.get("code") and update_dict["code"] != course.code:
            existing = await CourseRepository.get_course_by_code(db, update_dict["code"])
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A course with this code already exists")
        updated_course = await CourseRepository.update_course(db, course, update_dict)
        await db.commit()
        await db.refresh(updated_course)
        return CourseResponse.model_validate(updated_course)

    @staticmethod
    async def partial_update_course(
        db: AsyncSession,
        course_id: UUID,
        data: CoursePatch,
        current_user
    ):
        if current_user.role != UserRole.teacher:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can update courses")
        course = await CourseRepository.get_course_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        if course.teacher_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to modify this course")
        update_dict = data.model_dump(exclude_unset=True)
        if update_dict.get("code") and update_dict["code"] != course.code:
            existing = await CourseRepository.get_course_by_code(db, update_dict["code"])
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A course with this code already exists")
        updated_course = await CourseRepository.update_course(db, course, update_dict)
        await db.commit()
        await db.refresh(updated_course)
        return CourseResponse.model_validate(updated_course)

    @staticmethod
    async def delete_course(
        db: AsyncSession,
        course_id: UUID,
        current_user
    ):
        if current_user.role != UserRole.teacher:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can delete courses")
        course = await CourseRepository.get_course_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        if course.teacher_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this course")
        await CourseRepository.delete_course(db, course)
        await db.commit()
        return {"message": "Course deleted successfully"}
        
    


        
        





    

