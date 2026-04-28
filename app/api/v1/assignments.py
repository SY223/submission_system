from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User
from app.schemas.assignment_schema import *
from app.core.deps import get_async_db, get_current_user, require_student, require_teacher
from app.services.assignments_services import AssignmentService
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.services.comments_services import CommentService

assignment_router = APIRouter()


#Student submit an assignment
@assignment_router.post("/", response_model=AssignmentResponse, status_code=201)
async def create_assignment(
    student_name: str = Form(...),
    subject: str = Form(...),
    description: str = Form(None),
    course_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_student)
):
    assignment_data = AssignmentCreate(
        student_name=student_name,
        subject=subject, 
        description=description
    )
    
    return await AssignmentService.create_assignment(
        db=db,
        data=assignment_data,
        file=file,
        course_id=course_id,
    )

#Teacher gets all assignments
@assignment_router.get("/", response_model=list[AssignmentResponse])
async def get_all_assignments(
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)  # only admin can get all assignments
):
    return await AssignmentService.get_all_assignments(db)

#Teacher gets all assignments of a student
@assignment_router.get("/students/{name}/assignments/", response_model=list[AssignmentResponse])
async def get_student_assignments(
    name: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    return await AssignmentService.get_assignments_for_student(db, name)

#Teacher add comment to a student submission
@assignment_router.post("/{assignment_id}/comment",response_model=CommentResponse, status_code=201)
async def add_comment_to_assignment(
    assignment_id: str,
    teacher_name: str = Form(...),
    comment: str = Form(...),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_teacher)
):
    data = CommentCreate(
        teacher_name=teacher_name,
        comment=comment
    )

    return await CommentService.add_comment(
        db=db,
        assignment_id=assignment_id,
        data=data
    )
