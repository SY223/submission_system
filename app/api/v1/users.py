from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, get_async_db
from app.services.user_services import UserService
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate, UserPatch



user_router = APIRouter()

@user_router.post("/students/", response_model=UserRead, status_code=201)
async def create_student(
    data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.create_student(db, data)


@user_router.post("/teachers/", response_model=UserRead, status_code=201)
async def create_teacher(
    data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.create_teacher(db, data)
    
@user_router.get("/", response_model=list[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_async_db)):
    return await UserService.get_all_users(db)

@user_router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.get_user_by_id(db, user_id)

@user_router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id,
    data: UserUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.update_user(db, user_id, data)

@user_router.patch("/{user_id}", response_model=UserRead)
async def partial_update_user(
    user_id: str,
    data: UserPatch,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.partial_update_user(db, user_id, data)

@user_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    return await UserService.delete_user(db, user_id)

