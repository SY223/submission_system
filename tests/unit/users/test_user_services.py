import pytest
from fastapi import HTTPException
from app.services.user_services import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch
from app.models.user_model import User, UserRole

@pytest.mark.asyncio
async def test_create_student_success(db_session):
    data = UserCreate(
        full_name="Jane Doe",
        email="janedoe@aol.com"
    )
    result = await UserService.create_student(db_session, data)
    assert result.email == "janedoe@aol.com"
    assert result.role == UserRole.student
    assert result.id is not None

@pytest.mark.asyncio
async def test_create_teacher_success(db_session):
    data = UserCreate(
        full_name="Teacher Lewis",
        email="lewisteach@aol.com"
    )
    result = await UserService.create_teacher(db_session, data)
    assert result.role == UserRole.teacher

@pytest.mark.asyncio
async def test_create_user_duplicate_email_raises_400(db_session):
    existing_user = User(full_name="Badge Bend", email="taken@ex.com", role=UserRole.student)
    db_session.add(existing_user)
    await db_session.commit()

    data = UserCreate(full_name="Imposter Bend", email="taken@ex.com")
    with pytest.raises(HTTPException) as exc:
        await UserService.create_student(db_session, data)

    assert exc.value.status_code == 400
    assert "already exists" in exc.value.detail

@pytest.mark.asyncio
async def test_update_user_full_validation(db_session):
    user = User(full_name="Badge Bend", email="taken@ex.com", role=UserRole.student)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    update_data = UserUpdate(full_name="New Name", email="new@ex.com", role=UserRole.teacher)
    result = await UserService.update_user(db_session, user.id, update_data)

    assert result.full_name == "New Name"
    assert result.role == UserRole.teacher

@pytest.mark.asyncio
async def test_partial_update_whitespace_name_raises_422(db_session):
    user = User(
        full_name="Badge Bend",
        email="taken@ex.com",
        role=UserRole.student
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    patch_data = UserPatch(full_name="   ")
    with pytest.raises(HTTPException) as exc:
        await UserService.partial_update_user(db_session, user.id, patch_data)
    
    assert exc.value.status_code
    assert "cannot be empty" in exc.value.detail

@pytest.mark.asyncio
async def test_delete_user_success(db_session):
    user = User(
        full_name="Badge Bend",
        email="taken@ex.com",
        role=UserRole.student
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    response = await UserService.delete_user(db_session, user.id)
    assert response["message"] == "User deleted successfully"