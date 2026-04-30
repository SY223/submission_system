import io
import pytest
import uuid
from pathlib import Path
from fastapi import UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile
from uuid import UUID
from app.services.assignments_services import AssignmentService
from app.models.user_model import User, UserRole
from app.models.course_model import Course
from app.models.assignment_model import Assignment
from app.repositories.assignment_repo import AssignmentRepository
from app.schemas.assignment_schema import AssignmentCreate
from app.core.config import settings


#test if student could submit assignment
@pytest.mark.asyncio
async def test_create_assignment_success(tmp_path, db_session):
    settings.UPLOAD_DIR_ASSIGNMENTS = str(tmp_path)

    student = User(full_name="John Doe", email="john@example.com", role=UserRole.student)
    db_session.add(student)
    course = Course(
        title="Further Mathematics",
        code="MTH101",
        description="Basic algebra for engineering",
        teacher_id=uuid.uuid4()
    )
    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    file_content = b"test file assignment content"
    upload_file = StarletteUploadFile(filename="test.pdf", file=io.BytesIO(file_content))

    data = AssignmentCreate(
        student_name=student.full_name,
        subject="Algebra Week 2 Assessment",
        description="I have attached the solutions for my week 2 assessment"
    )

    assignment = await AssignmentService.create_assignment(
        db=db_session,
        data=data,
        file=upload_file,
        course_id=course.id
    )

    assert assignment.student_id == student.id
    assert assignment.course_id == course.id
    assert assignment.original_filename == "test.pdf"

    saved_path = Path(assignment.file_path)
    assert saved_path.exists()
    assert saved_path.read_bytes() == file_content


@pytest.mark.asyncio
async def test_create_assignment_course_not_found(tmp_path, db_session):
    settings.UPLOAD_DIR_ASSIGNMENTS = str(tmp_path)

    student = User(full_name="Jane Doe", email="john@example.com", role=UserRole.student)
    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)

    upload_file = StarletteUploadFile(filename="file.pdf", file=io.BytesIO(b"data"))

    data = AssignmentCreate(
        student_name=student.full_name,
        subject="Algebra Week 2 Assessment",
        description="I have attached the solutions for my week 2 assessment"
    )

    with pytest.raises(Exception) as exc:
        await AssignmentService.create_assignment(
            db=db_session,
            data=data,
            file=upload_file,
            course_id=uuid.uuid4(),  # nonexistent
        )

    assert "Course not found" in str(exc.value)

@pytest.mark.asyncio
async def test_get_all_assignments(db_session):
    student = User(full_name="Alice", email="alice@example.com", role=UserRole.student)
    course = Course(title="History", code="HIS101", description="World", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    # Assignments
    a1 = Assignment(course_id=course.id, student_id=student.id, subject="Egypt", file_path="/tmp/egypt.pdf", original_filename="egypt.pdf")
    a2 = Assignment(course_id=course.id, student_id=student.id, subject="Rome", file_path="/tmp/rome.pdf", original_filename="rome.pdf")
    db_session.add_all([a1, a2])
    await db_session.commit()

    results = await AssignmentService.get_all_assignments(db_session)

    assert len(results) == 2
    subjects = {a.subject for a in results}
    assert "Egypt" in subjects
    assert "Rome" in subjects

@pytest.mark.asyncio
async def test_get_assignments_for_student(db_session):
    student = User(full_name="Chris", email="chris@example.com", role=UserRole.student)
    course = Course(title="Geography", code="GEO101", description="Maps", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    assignment = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Maps",
        file_path="/tmp/chrismaps.pdf",
        original_filename="chrismaps.pdf"
    )
    db_session.add(assignment)
    await db_session.commit()

    results = await AssignmentService.get_assignments_for_student(db_session, "Chris")

    assert len(results) == 1
    assert results[0].subject == "Maps"