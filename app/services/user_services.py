from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import UserRole
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate, UserPatch
from app.repositories.user_repo import UserRepository
import uuid

class UserService:
    @staticmethod
    async def _create_user(db: AsyncSession, data: UserCreate, role: UserRole):
        user_dict = data.model_dump()
        user_dict["role"] = role
    
        existing = await UserRepository.get_user_by_email(db, user_dict["email"])
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists")
        if user_dict["full_name"] is not None:
            if not user_dict["full_name"].strip():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Full name cannot be empty")
        user = await UserRepository.create_user(db, user_dict)
        return UserRead.model_validate(user)
    
    @staticmethod
    async def create_student(db: AsyncSession, data: UserCreate):
        return await UserService._create_user(db, data, UserRole.student)
    
    @staticmethod
    async def create_teacher(db: AsyncSession, data: UserCreate):
        return await UserService._create_user(db, data, UserRole.teacher)
    
    @staticmethod
    async def get_all_users(db: AsyncSession):
        users = await UserRepository.get_all_users(db)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users in database")
        return [UserRead.model_validate(u) for u in users]

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id):
        user = await UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.model_validate(user)

    @staticmethod
    async def update_user(db: AsyncSession, user_id, data: UserUpdate):
        user = await UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if data.full_name is not None:
            if not data.full_name.strip():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Full name cannot be empty")
        if data.email is not None:
            if data.email != user.email:
                existing = await UserRepository.get_user_by_email(db, data.email)
                if existing:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists")
        updated_user = await UserRepository.update_user(db, user, data)
        return UserRead.model_validate(updated_user)
    
    @staticmethod
    async def partial_update_user(db: AsyncSession, user_id: str, data: UserPatch):
        user = await UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        update_data = data.model_dump(exclude_unset=True)
        if "email" in update_data:
            new_email = update_data["email"].lower()
            if new_email != user.email:
                existing = await UserRepository.get_user_by_email(db, new_email)
                if existing:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists")
            update_data["email"] = new_email
        if "full_name" in update_data:
            if not update_data["full_name"].strip():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Full name cannot be empty")
            update_data["full_name"] = update_data["full_name"].lower()
        updated_user = await UserRepository.partial_update_user(db, user, update_data)
        return UserRead.model_validate(updated_user)


    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: str):
        user = await UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await UserRepository.delete_user(db, user)
        return {"message": "User deleted successfully"}
