from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db, get_current_user 
from app.schemas.course_schema import (
    CourseCreate, CourseResponse, CourseUpdate, CoursePatch
)
from app.services.courses_services import CourseService
from app.models.user_model import User
from uuid import UUID

course_router = APIRouter()


@course_router.post("/", response_model=CourseResponse, status_code=201)
async def create_course(
    data: CourseCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await CourseService.create_course(db, data, current_user)


@course_router.get("/", response_model=list[CourseResponse])
async def get_all_courses(
    db: AsyncSession = Depends(get_async_db)
):
    return await CourseService.get_all_courses(db)

@course_router.get("/code/{course_code}", response_model=CourseResponse)
async def get_course_by_code(
    course_code: str,
    db: AsyncSession = Depends(get_async_db)
):
    return await CourseService.get_course_by_code(db, course_code)


@course_router.get("/id/{course_id}", response_model=CourseResponse)
async def get_course_by_id(
    course_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    return await CourseService.get_course_by_id(db, course_id)


@course_router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: UUID,
    data: CourseUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    return await CourseService.update_course(db, course_id, data, current_user)

@course_router.patch("/{course_id}", response_model=CourseResponse)
async def partial_update_course(
    course_id: UUID,
    data: CoursePatch,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    return await CourseService.partial_update_course(db, course_id, data, current_user)

@course_router.delete("/{course_id}")
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    return await CourseService.delete_course(db, course_id, current_user) 

