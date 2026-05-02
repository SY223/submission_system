from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token, create_refresh_token, hash_password
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.auth_schema import LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user_schema import UserCreate, UserRole, UserRead
from app.models.user_model import User


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, data: UserCreate):
        user_dict = data.model_dump()
        role = user_dict.get("role", UserRole.student)
        user_dict["role"] = role
 
        if len(user_dict["password"]) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at least 8 characters long"
            )

        if len(user_dict["password"].encode("utf-8")) > 72:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password cannot exceed 72 characters"
            )
        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
        existing = await UserRepository.get_user_by_email(db, user_dict["email"])
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )
        if user_dict["full_name"] is not None:
            if not user_dict["full_name"].strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Full name cannot be empty"
                )
        user = await UserRepository.create_user(db, user_dict)
        await db.commit()
        await db.refresh(user)
        return UserRead.model_validate(user)

    @staticmethod
    async def login(db: AsyncSession, email: str, password: str):
        user = await UserRepository.get_user_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled"
            )
        #JWT access token
        access_token = create_access_token(
            {"sub": str(user.id), "role": user.role.value},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_refresh_token({"sub": str(user.id)})
        user.refresh_token = refresh_token
        await db.commit()
        await db.refresh(user)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    @staticmethod
    async def refresh(
        data: RefreshRequest,
        db: AsyncSession
    ):
        incoming_token = data.refresh_token
        try:
            payload = jwt.decode(incoming_token, settings.JWT_REFRESH_SECRET, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        user = await UserRepository.get_user_by_id(db, user_id)
        if not user or user.refresh_token != incoming_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired or invalid"
            )
        new_refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role.value})
        user.refresh_token = new_refresh_token
        new_access_token = create_access_token({"sub": str(user.id), "role": user.role.value})

        await db.commit()
        await db.refresh(user)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )
    
    @staticmethod
    async def logout(db: AsyncSession, user):
        user.refresh_token = None
        await db.commit()
        return {
            "message": "Logged out successfully"
        }
