from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user_model import User


class UserRepository:
    @staticmethod
    async def create_user(db: AsyncSession, data):
        new_user = User(
            full_name=data["full_name"],
            email=data["email"],
            role=data["role"]
        )
        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first() # type: ignore

    @staticmethod
    async def get_user_by_full_name(db: AsyncSession, full_name: str):
        result = await db.execute(
            select(User).where(func.lower(User.full_name) == full_name.lower())
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_all_users(db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    @staticmethod
    async def update_user(db: AsyncSession, user: User, data):
        user.full_name = data.full_name
        user.email = data.email
        user.role = data.role
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def partial_update_user(db: AsyncSession, user: User, update_data: dict):
        for field, value in update_data.items():
            setattr(user, field, value)
        await db.flush()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user: User):
        await db.delete(user)
        await db.flush()