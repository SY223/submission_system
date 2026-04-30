import io
import uuid
import pytest
from httpx import AsyncClient
from app.models.user_model import User, UserRole
from app.models.course_model import Course
from app.models.assignment_model import Assignment
from app.schemas.assignment_schema import AssignmentCreate
from app.main import app
from app.core.deps import get_current_user, require_student, require_teacher

def override_student(user):
    app.dependency_overrides[require_student] = lambda: user
    app.dependency_overrides[get_current_user] = lambda: user


def override_teacher(user):
    app.dependency_overrides[require_teacher] = lambda: user
    app.dependency_overrides[get_current_user] = lambda: user
#Test student can submit
@pytest.mark.asyncio
async def test_student_can_submit_assignment(tmp_path, client: AsyncClient, db_session):
    from app.core.config import settings
    settings.UPLOAD_DIR_ASSIGNMENTS = str(tmp_path)

    student = User(full_name="John Doe", email="john@example.com", role=UserRole.student)
    course = Course(title="Math", code="MTH101", description="Algebra", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    override_student(student)

    file_content = b"assignment content"
    file = ("file", ("assignment.pdf", io.BytesIO(file_content), "application/pdf"))

    data = {
        "student_name": student.full_name,
        "subject": "Week 1 Algebra",
        "description": "My submission",
        "course_id": str(course.id),
    }
    response = await client.post("/api/v1/assignments/", data=data, files=[file])

    assert response.status_code == 201
    body = response.json()
    assert body["student_id"] == str(student.id)
    assert body["course_id"] == str(course.id)
    assert body["original_filename"] == "assignment.pdf"

    # File saved?
    saved_path = body["file_path"]
    assert tmp_path.joinpath("assignment.pdf").exists()

#Test teacher GET student assignment
@pytest.mark.asyncio
async def test_teacher_gets_assignments_for_student(client: AsyncClient, db_session):
    teacher = User(full_name="Prof McGonagall", email="mcg@hogwarts.edu", role=UserRole.teacher)
    student = User(full_name="Hermione Granger", email="hermione@hogwarts.edu", role=UserRole.student)
    db_session.add_all([teacher, student])
    await db_session.commit()

    course = Course(title="Transfiguration", code="TRN101", description="Magic", teacher_id=teacher.id)
    db_session.add(course)
    await db_session.commit()

    assignment = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Cat Transformation",
        file_path="/tmp/cat.pdf",
        original_filename="cat.pdf"
    )
    db_session.add(assignment)
    await db_session.commit()

    override_teacher(teacher)

    response = await client.get(f"/api/v1/assignments/students/{student.full_name.strip()}/assignments/")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["subject"] == "Cat Transformation"


#Test teacher POST comment on assignment
@pytest.mark.asyncio
async def test_teacher_adds_comments_on_assignments(client: AsyncClient, db_session):
    teacher = User(full_name="Prof McGonagall", email="mcg@hogwarts.edu", role=UserRole.teacher)
    student = User(full_name="Hermione Granger", email="hermione@hogwarts.edu", role=UserRole.student)
    db_session.add_all([teacher, student])
    await db_session.commit()

    course = Course(title="Transfiguration", code="TRN101", description="Magic", teacher_id=teacher.id)
    db_session.add(course)
    await db_session.commit()

    assignment = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Cat Transformation",
        file_path="/tmp/cat.pdf",
        original_filename="cat.pdf"
    )
    db_session.add(assignment)
    await db_session.commit()

    override_teacher(teacher)
    data = {
        "teacher_name": teacher.full_name,
        "content": "Excellent work"
    }

    response = await client.post(f"/api/v1/assignments/{assignment.id}/comment", data=data)
    assert response.status_code == 201
    body = response.json()
    assert body["teacher_name"] == teacher.full_name
    assert body["content"] == "Excellent work"
    assert body["assignment_id"] == str(assignment.id)