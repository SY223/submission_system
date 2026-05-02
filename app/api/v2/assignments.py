from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.assignment_schema import *
from app.core.deps import get_async_db, auth_get_current_user, auth_require_teacher, auth_require_student
from app.services.assignments_services import AssignmentService
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.services.comments_services import CommentService
import uuid

assignment_router_v2 = APIRouter()


#Student submit an assignment
@assignment_router_v2.post(
    "/", 
    response_model=AssignmentResponse, 
    status_code=201,
    dependencies=[Depends(auth_require_student)]
)
async def create_assignment(
    student_name: str = Form(...),
    subject: str = Form(...),
    description: str = Form(None),
    course_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(auth_get_current_user)
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

#Teacher or admin gets all assignments
@assignment_router_v2.get(
    "/", 
    response_model=list[AssignmentResponse],
    dependencies=[Depends(auth_require_teacher)]
)
async def get_all_assignments(
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(auth_get_current_user) 
):
    return await AssignmentService.get_all_assignments(db)

#Teacher or admin gets all assignments of a student
@assignment_router_v2.get(
    "/students/{name}/assignments/", 
    response_model=list[AssignmentResponse],
    dependencies=[Depends(auth_require_teacher)]
)
async def get_student_assignments(
    name: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(auth_get_current_user)
):
    return await AssignmentService.get_assignments_for_student(db, name)

#Teacher add comment to a student submission
@assignment_router_v2.post(
    "/{assignment_id}/comment",
    response_model=CommentResponse,
    status_code=201,
    dependencies=[Depends(auth_require_teacher)]
)
async def add_comment_to_assignment(
    assignment_id: str,
    teacher_name: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(auth_require_teacher)
):
    data = CommentCreate(
        teacher_name=teacher_name,
        content=content
    )
    saved_comment = await CommentService.add_comment(
        db=db,
        assignment_id=uuid.UUID(assignment_id),
        data=data
    )
    return CommentResponse(
        id=saved_comment.id,
        assignment_id=saved_comment.assignment_id,
        teacher_name=saved_comment.teacher.full_name,
        content=saved_comment.content,
        created_at=saved_comment.created_at
    ) # type: ignore
