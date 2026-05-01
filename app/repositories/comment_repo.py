from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.comment_model import Comment

class CommentRepository:
    @staticmethod
    async def create_comment(db: AsyncSession, data: dict):
        comment = Comment(**data)
        db.add(comment)
        await db.flush()
        await db.refresh(comment)
        return comment