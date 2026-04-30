import pytest
from fastapi import HTTPException
from app.services.courses_services import CourseService
from app.schemas.course_schema import CourseCreate, CourseUpdate
from app.models.user_model import User, UserRole
from app.models.course_model import Course

@pytest.mark.asyncio
async def test_create_course_success(db_session):
    teacher = User(full_name="Professor Snape", email="potions@hogwarts.edu", role=UserRole.teacher)
    db_session.add(teacher)
    await db_session.commit()
    
    course_in = CourseCreate(
        title="Advanced Driving",
        code="DRV401",
        description="Learning large vehicle driving fundamentals"
    )
    result = await CourseService.create_course(db_session, course_in, current_user=teacher)
    assert result.code == "DRV401"
    assert result.teacher_id == teacher.id

@pytest.mark.asyncio
async def test_create_course_as_student_fails(db_session):
    student = User(full_name="Bob Manner", email="bob@test.com", role=UserRole.student)
    db_session.add(student)
    await db_session.commit()
    
    course_in = CourseCreate(title="Test of Light", code="TST101")
    
    with pytest.raises(HTTPException) as exc:
        await CourseService.create_course(db_session, course_in, current_user=student)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
async def test_create_course_duplicate_code_raises_400(db_session):
    teacher = User(full_name="Professor Snape", email="potions@hogwarts.edu", role=UserRole.teacher)
    db_session.add(teacher)
    await db_session.commit()
    
    existing_course = Course(title="First Course", code="DUP121", teacher_id=teacher.id)
    db_session.add(existing_course)
    await db_session.commit()
    
    new_course_in = CourseCreate(title="Second Course", code="DUP121", teacher_id=teacher.id) # type: ignore
    with pytest.raises(HTTPException) as exc:
        await CourseService.create_course(db_session, new_course_in, current_user=teacher)
    
    assert exc.value.status_code == 400
    assert "already exists" in exc.value.detail

@pytest.mark.asyncio
async def test_get_all_courses_empty_raises_404(db_session):
    with pytest.raises(HTTPException) as exc:
        await CourseService.get_all_courses(db_session)
    
    assert exc.value.status_code == 404