from app.core.db import SessionLocal
from app.core.db_async import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header, HTTPException, status, Depends
from app.models.user_model import UserRole
from app.repositories.user_repo import UserRepository
from uuid import UUID

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(
    x_user_id: UUID = Header(..., alias="X-User-Id"),
    db: AsyncSession = Depends(get_async_db)
    ):
  
    user_id = str(x_user_id)
    user = await UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

async def require_student(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students are allowed to submit assignments"
        )
    return current_user

async def require_teacher(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers are allowed to comment on assignments"
        )
    return current_user