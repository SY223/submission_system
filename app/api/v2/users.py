from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db, auth_get_current_user, auth_require_teacher_or_admin, auth_require_admin
from app.services.user_services import UserService
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate, UserPatch



user_router_v2 = APIRouter()

# @user_router_v2.post("/students/", response_model=UserRead, status_code=201)
# async def create_student(
#     data: UserCreate,
#     db: AsyncSession = Depends(get_async_db)
# ):
#     """Register student"""
#     return await UserService.create_student(db, data)


# @user_router_v2.post("/teachers/", response_model=UserRead, status_code=201)
# async def create_teacher(
#     data: UserCreate,
#     db: AsyncSession = Depends(get_async_db)
# ):
#     """Register teacher"""
#     return await UserService.create_teacher(db, data)

#Only teacher and admin get all users
@user_router_v2.get("/", response_model=list[UserRead], dependencies=[Depends(auth_require_teacher_or_admin)])
async def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_async_db)
    ):
    return await UserService.get_all_users(db, skip, limit)


@user_router_v2.get("/{user_id}", response_model=UserRead, dependencies=[Depends(auth_require_teacher_or_admin)])
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.get_user_by_id(db, user_id)

@user_router_v2.put("/{user_id}", response_model=UserRead, dependencies=[Depends(auth_require_admin)])
async def update_user(
    user_id,
    data: UserUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.update_user(db, user_id, data)

@user_router_v2.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(auth_require_admin)])
async def partial_update_user(
    user_id: str,
    data: UserPatch,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.partial_update_user(db, user_id, data)

@user_router_v2.delete("/{user_id}", dependencies=[Depends(auth_require_admin)])
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.delete_user(db, user_id)

