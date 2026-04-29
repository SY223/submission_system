import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from app.main import app # Import your main FastAPI app
from app.core.deps import get_async_db



# In-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    from app.models.user_model import User
    from app.core.db_async import Base

    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    await engine.dispose()

@pytest.fixture
async def client(db_session):
    async def override_get_async_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_async_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()