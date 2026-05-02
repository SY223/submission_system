from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import jwt, JWTError
from app.core.db import SessionLocal
from app.core.db_async import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header, HTTPException, status, Depends
from app.models.user_model import UserRole
from app.repositories.user_repo import UserRepository
from uuid import UUID


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login")

#sync
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

#AUTH RESOURCE
async def auth_get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise credentials_exception
    return user

async def auth_require_teacher(current_user = Depends(auth_get_current_user)):
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required"
        )
    return current_user

async def auth_require_student(current_user = Depends(auth_get_current_user)):
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )
    return current_user

async def auth_require_admin(current_user = Depends(auth_get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

async def auth_require_teacher_or_admin(current_user = Depends(auth_get_current_user)):
    if current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher or admin access required"
        )
    return current_user
