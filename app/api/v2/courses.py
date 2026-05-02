from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db, auth_get_current_user, auth_require_teacher, auth_require_teacher_or_admin
from app.schemas.course_schema import (
    CourseCreate, CourseResponse, CourseUpdate, CoursePatch
)
from app.services.courses_services import CourseService
from app.models.user_model import User
from uuid import UUID

course_router_v2 = APIRouter()


#Only teacher could create courses
@course_router_v2.post(
    "/", 
    response_model=CourseResponse, 
    status_code=201,
    dependencies=[Depends(auth_require_teacher)]
)
async def create_course(
    data: CourseCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(auth_get_current_user)

):
    return await CourseService.create_course(db, data, current_user)


@course_router_v2.get("/", response_model=list[CourseResponse])
async def get_all_courses(
    db: AsyncSession = Depends(get_async_db)
):
    return await CourseService.get_all_courses(db)

@course_router_v2.get("/code/{course_code}", response_model=CourseResponse)
async def get_course_by_code(
    course_code: str,
    db: AsyncSession = Depends(get_async_db)
):
    return await CourseService.get_course_by_code(db, course_code)


@course_router_v2.get("/id/{course_id}", response_model=CourseResponse)
async def get_course_by_id(
    course_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    return await CourseService.get_course_by_id(db, course_id)


@course_router_v2.put(
    "/{course_id}", 
    response_model=CourseResponse,
    dependencies=[Depends(auth_require_teacher_or_admin)]
)
async def update_course(
    course_id: UUID,
    data: CourseUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(auth_get_current_user)
):
    return await CourseService.update_course(db, course_id, data, current_user)

@course_router_v2.patch(
    "/{course_id}", 
    response_model=CourseResponse,
    dependencies=[Depends(auth_require_teacher_or_admin)]
)
async def partial_update_course(
    course_id: UUID,
    data: CoursePatch,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(auth_get_current_user)
):
    return await CourseService.partial_update_course(db, course_id, data, current_user)

@course_router_v2.delete(
    "/{course_id}",
    dependencies=[Depends(auth_require_teacher_or_admin)]
)
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(auth_get_current_user)
):
    return await CourseService.delete_course(db, course_id, current_user) 

