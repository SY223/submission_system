import pytest
from uuid import uuid4
from app.models.course_model import Course
from app.models.user_model import User, UserRole
from app.repositories.course_repo import CourseRepository

@pytest.mark.asyncio
async def test_create_course_success(db_session):
    teacher = User(
        full_name="Professor Snape",
        email="potions@hogwarts.edu",
        role=UserRole.teacher
    )
    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

    course_data = {
        "title": "Potions 101",
        "code": "POT101",
        "description": "Brewing basics.",
        "teacher_id": teacher.id
    }
    course = await CourseRepository.create_course(db_session, course_data)
    assert course.id is not None
    assert course.title == "Potions 101"
    assert course.teacher_id == teacher.id

@pytest.mark.asyncio
async def test_get_course_by_code(db_session):
    teacher = User(
        full_name="Professor Snape",
        email="potions@hogwarts.edu",
        role=UserRole.teacher
    )
    db_session.add(teacher)
    await db_session.commit()
    
    course = Course(title="Physics", code="PHY125", teacher_id=teacher.id)
    db_session.add(course)
    await db_session.commit()

    fetched = await CourseRepository.get_course_by_code(db_session, "PHY125")
    assert fetched is not None
    assert fetched.title == "Physics"

@pytest.mark.asyncio
async def test_update_course(db_session):
    teacher = User(full_name="Professor Snape", email="potions@hogwarts.edu", role=UserRole.teacher)
    db_session.add(teacher)
    await db_session.commit()
    
    course = Course(title="Old Title", code="OLD155", teacher_id=teacher.id)
    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    updated_data = {"title": "New Title"}
    updated_course = await CourseRepository.update_course(db_session, course, updated_data)

    assert updated_course.title == "New Title"

@pytest.mark.asyncio
async def test_delete_course(db_session):
    teacher = User(full_name="Professor Snape", email="potions@hogwarts.edu", role=UserRole.teacher)
    db_session.add(teacher)
    await db_session.commit()
    
    course = Course(title="Old Title", code="OLD155", teacher_id=teacher.id)
    db_session.add(course)
    await db_session.commit()

    await CourseRepository.delete_course(db_session, course)
    
    fetched = await CourseRepository.get_course_by_id(db_session, course.id)
    assert fetched is None