import pytest
import uuid
from app.models.assignment_model import Assignment
from app.models.user_model import User, UserRole
from app.models.course_model import Course
from app.repositories.assignment_repo import AssignmentRepository


@pytest.mark.asyncio
async def test_create_assignment(db_session):
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

    data = {
        "course_id": course.id,
        "student_id": student.id,
        "subject": f"{student.full_name} Algbera Week 2 Assignment",
        "description": "Assignment 1",
        "file_path": "/uploads/assignments/file1.pdf",
        "original_filename": "file1.pdf"
    }
    assignment = await AssignmentRepository.create_assignment(db_session, data)
    assert assignment.id is not None
    assert assignment.student_id == student.id
    assert assignment.course_id == course.id
    assert assignment.subject == "John Doe Algbera Week 2 Assignment"

@pytest.mark.asyncio
async def test_get_assignment_by_id(db_session):
    student = User(full_name="John Doe", email="john@example.com", role=UserRole.student)
    course = Course(title="Further Mathematics", code="MTH101", description="Basic algebra for engineering", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    assignment = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Linear Algebra",
        description="Algebra",
        file_path="/uploads/assignments/lab_algebra.pdf",
        original_filename="lab_algebra.pdf"
    )
    db_session.add(assignment)
    await db_session.commit()
    await db_session.refresh(assignment)

    fetched = await AssignmentRepository.get_assignment_by_id(db_session, assignment.id)
    assert fetched is not None
    assert fetched.id == assignment.id
    assert fetched.subject == "Linear Algebra"

#Student GET all assignments
@pytest.mark.asyncio
async def test_get_all_assignments(db_session):
    student = User(full_name="John Doe", email="john@example.com", role=UserRole.student)
    course = Course(title="Further Mathematics", code="MTH101", description="Basic algebra for engineering", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    a1 = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Linear Algebra",
        description="Algebra",
        file_path="/uploads/assignments/lab_algebra.pdf",
        original_filename="lab_algebra.pdf"
    )

    a2 = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Trigonometry",
        description="Trigonometry Lab work",
        file_path="/uploads/assignments/trigo.pdf",
        original_filename="trigo.pdf"
    )
    db_session.add_all([a1, a2])
    await db_session.commit()

    assignments = await AssignmentRepository.get_all_assignments(db_session)
    assert len(assignments) == 2
    subjects = {a.subject for a in assignments}
    assert "Linear Algebra" in subjects
    assert "Trigonometry" in subjects

#GET assignment by student_id
@pytest.mark.asyncio
async def test_get_assignments_by_student_id(db_session):
    student = User(full_name="John Doe", email="john@example.com", role=UserRole.student)
    course = Course(title="Further Mathematics", code="MTH101", description="Basic algebra for engineering", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    assignment = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Linear Algebra",
        description="Algebra",
        file_path="/uploads/assignments/lab_algebra.pdf",
        original_filename="lab_algebra.pdf"
    )

    db_session.add(assignment)
    await db_session.commit()

    results = await AssignmentRepository.get_assignments_by_student_id(db_session, student.id)

    assert len(results) == 1
    assert results[0].subject == "Linear Algebra"

#GET assignment by student_name
@pytest.mark.asyncio
async def test_get_assignments_by_student_name(db_session):
    student = User(full_name="John Doe", email="john@example.com", role=UserRole.student)
    course = Course(title="Further Mathematics", code="MTH101", description="Basic algebra for engineering", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    assignment = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Statistics",
        description="All about statistics",
        file_path="/uploads/assignments/statistics.pdf",
        original_filename="statistics.pdf"
    )

    db_session.add(assignment)
    await db_session.commit()

    results = await AssignmentRepository.get_assignments_by_student_name(db_session, "John Doe")

    assert len(results) == 1
    assert results[0].subject == "Statistics"

#Confirm student has submitted
@pytest.mark.asyncio
async def test_student_has_submitted(db_session):
    student = User(full_name="John Doe", email="john@example.com", role=UserRole.student)
    course = Course(title="Further Mathematics", code="MTH101", description="Basic algebra for engineering", teacher_id=uuid.uuid4())
    db_session.add_all([student, course])
    await db_session.commit()
    await db_session.refresh(student)
    await db_session.refresh(course)

    assignment = Assignment(
        course_id=course.id,
        student_id=student.id,
        subject="Statistics",
        description="All about statistics",
        file_path="/uploads/assignments/statistics.pdf",
        original_filename="statistics.pdf"
    )

    db_session.add(assignment)
    await db_session.commit()

    exists = await AssignmentRepository.student_has_submitted(db_session, student.id, course.id)
    assert exists is not None
    assert exists.subject == "Statistics"