import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.repositories.user_repo import UserRepository
from app.models.user_model import User, UserRole

@pytest.mark.asyncio
async def test_create_user_success(db_session: AsyncSession):
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "role": "student"
    }
    new_user = await UserRepository.create_user(db_session, user_data)
    assert new_user.id is not None
    assert new_user.email == "john@example.com"
    assert new_user.full_name == "John Doe"
   
@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession):
    email = "billian@example.com"
    user = User(full_name="Billian Pan", email=email, role="teacher")
    db_session.add(user)
    await db_session.commit()

    fetched_user = await UserRepository.get_user_by_email(db_session, email)
    assert fetched_user is not None
    assert fetched_user.email == email

@pytest.mark.asyncio
async def test_get_user_by_full_name_case_insensitive(db_session: AsyncSession):
    user = User(full_name="Alice Smith", email="alice.smith@box.ng", role="student")
    db_session.add(user)
    await db_session.commit()

    fetched_user = await UserRepository.get_user_by_full_name(db_session, "ALICE smith")

    assert fetched_user is not None
    assert fetched_user.full_name == "Alice Smith"

@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession):
    user = User(full_name="Alice Smith", email="alice.smith@box.ng", role="student")
    db_session.add(user)
    await db_session.commit()

    class UpdateSchema:
        full_name = "New Name"
        email = "new.name@aol.com"
        role = "teacher"

    updated_user = await UserRepository.update_user(db_session, user, UpdateSchema)

    assert updated_user.full_name == "New Name"
    assert updated_user.role == "teacher"


@pytest.mark.asyncio
async def test_partial_update_user(db_session):
    user = User(full_name="Asma Cotton", email="asma.cotton@box.ng", role="student")
    db_session.add(user)
    await db_session.commit()

    payload = {"full_name": "Summer Winter"}
    updated_user = await UserRepository.partial_update_user(db_session, user, payload)
    assert updated_user.full_name == "Summer Winter"
    assert updated_user.email == "asma.cotton@box.ng"
    assert updated_user.role == "student"


@pytest.mark.asyncio
async def test_delete_user(db_session):
    user = User(full_name="Alice Smith", email="alice.smith@box.ng", role="student")
    db_session.add(user)
    await db_session.commit()

    await UserRepository.delete_user(db_session, user)
    check_deleted = await UserRepository.get_user_by_email(db_session, "alice.smith@box.ng")
    assert check_deleted is None
