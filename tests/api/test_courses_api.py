import pytest
from app.main import app
from app.core.deps import get_current_user
from app.models.user_model import User, UserRole
from app.models.course_model import Course

@pytest.mark.asyncio
async def test_create_course_as_teacher(client, db_session):
    teacher = User(full_name="Sam Lacey", email="samlacey@test.com", role=UserRole.teacher)
    db_session.add(teacher)
    await db_session.commit()

    app.dependency_overrides[get_current_user] = lambda: teacher
    course_payload = {
        "title": "Advanced Driving",
        "code": "DRV401",
        "teacher_id": str(teacher.id)
    }
    response = await client.post("/api/v1/courses/", json=course_payload)


    assert response.status_code == 201
    assert response.json()["title"] == "Advanced Driving"

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_course_forbidden_for_student(client, db_session):
    student = User(full_name="Bob Manner", email="bob@test.com", role=UserRole.student)
    db_session.add(student)
    await db_session.commit()

    app.dependency_overrides[get_current_user] = lambda: student
    payload = {"title": "Advanced Driving", "code": "DRV401", "teacher_id": str(student.id)}
    response = await client.post("/api/v1/courses/", json=payload)

    assert response.status_code == 403
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_course_by_both_code_id(client, db_session):
    teacher = User(full_name="Sam", email="sam@test.com", role=UserRole.teacher)
    db_session.add(teacher)
    await db_session.commit()

    new_course = Course(title="Test of Light", code="TST101", teacher_id=teacher.id)
    db_session.add(new_course)
    await db_session.commit()
    await db_session.refresh(new_course)

    response_code = await client.get(f"/api/v1/courses/code/{new_course.code}")
    assert response_code.status_code == 200
    assert response_code.json()["title"] == "Test of Light"

    response_id = await client.get(f"/api/v1/courses/id/{str(new_course.id)}")
    assert response_id.status_code == 200
    assert response_id.json()["title"] == "Test of Light"

#PUT TEST
@pytest.mark.asyncio
async def test_only_owner_teacher_can_update_course(client, db_session):
    owner = User(full_name="Sam Lacey", email="samlacey@test.com", role=UserRole.teacher)
    other_teacher = User(full_name="Other Prof", email="other@test.com", role=UserRole.teacher)
    student = User(full_name="Bob Manner", email="bob@test.com", role=UserRole.student)
    
    db_session.add_all([owner, other_teacher, student])
    await db_session.commit()
    
    course = Course(title="Original Title", code="ORG101", teacher_id=owner.id)
    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    update_payload = {"title": "fundamentals of statistics", "code": "BHM101"}
    # The Student fails
    app.dependency_overrides[get_current_user] = lambda: student
    res_student = await client.put(f"/api/v1/courses/{course.id}", json=update_payload)
    assert res_student.status_code == 403

    #The Wrong Teacher fails
    app.dependency_overrides[get_current_user] = lambda: other_teacher
    res_wrong_prof = await client.put(f"/api/v1/courses/{course.id}", json=update_payload)
    assert res_wrong_prof.status_code == 403

    #The Owner succeeds
    app.dependency_overrides[get_current_user] = lambda: owner
    res_owner = await client.put(f"/api/v1/courses/{course.id}", json=update_payload)
    assert res_owner.status_code == 200
    assert res_owner.json()["title"] == "fundamentals of statistics"

    app.dependency_overrides.clear()

#PATCH TEST
@pytest.mark.asyncio
async def test_only_owner_teacher_can_patch_course(client, db_session):
    owner = User(full_name="Sam Lacey", email="samlacey@test.com", role=UserRole.teacher)
    other_teacher = User(full_name="Other Prof", email="other@test.com", role=UserRole.teacher)
    student = User(full_name="Bob Manner", email="bob@test.com", role=UserRole.student)
    
    db_session.add_all([owner, other_teacher, student])
    await db_session.commit()
    
    course = Course(title="Original Title", code="ORG101", teacher_id=owner.id)
    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    update_payload = {"title": "fundamentals of statistics"}
    # The Student fails
    app.dependency_overrides[get_current_user] = lambda: student
    res_student = await client.patch(f"/api/v1/courses/{course.id}", json=update_payload)
    assert res_student.status_code == 403

    #The Wrong Teacher fails
    app.dependency_overrides[get_current_user] = lambda: other_teacher
    res_wrong_prof = await client.patch(f"/api/v1/courses/{course.id}", json=update_payload)
    assert res_wrong_prof.status_code == 403

    #The Owner succeeds
    app.dependency_overrides[get_current_user] = lambda: owner
    res_owner = await client.patch(f"/api/v1/courses/{course.id}", json=update_payload)
    assert res_owner.status_code == 200
    assert res_owner.json()["title"] == "fundamentals of statistics"
    assert res_owner.json()["code"] == "ORG101"
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_course_as_teacher(client, db_session):
    teacher = User(
        full_name="Professor Snape",
        email="snape@hogwarts.edu",
        role=UserRole.teacher
    )
    db_session.add(teacher)
    await db_session.commit()
    await db_session.refresh(teacher)

    app.dependency_overrides[get_current_user] = lambda: teacher

    course = Course(
        title="Potions Control",
        code="PTN101",
        description="Advanced potion making",
        teacher_id=teacher.id
    )
    db_session.add(course)
    await db_session.commit()
    await db_session.refresh(course)

    response = await client.delete(f"/api/v1/courses/{course.id}")
    assert response.status_code == 200

    deleted = await db_session.get(Course, course.id)
    assert deleted is None