
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings



DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in environment variables or fallback!")

engine = create_engine(
    DATABASE_URL,
    echo= True if settings.ENVIRONMENT == "DEBUG" else False,  # Logs SQL — disable in production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern Base class (SQLAlchemy 2.x)
class Base(DeclarativeBase):
    pass

from app.models import *