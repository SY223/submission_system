
import anyio
from fastapi import HTTPException, status, UploadFile
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.assignment_schema import AssignmentCreate, AssignmentResponse
from app.repositories.assignment_repo import AssignmentRepository
from app.repositories.user_repo import UserRepository
from app.repositories.course_repo import CourseRepository
from app.core.config import settings

class AssignmentService:
    @staticmethod
    async def create_assignment(
        db: AsyncSession,
        data: AssignmentCreate,
        file: UploadFile,
        course_id,
    ):
        
        upload_dir = settings.UPLOAD_DIR_ASSIGNMENTS
        if not upload_dir:
            raise RuntimeError("UPLOAD_DIR_ASSIGNMENTS is not configured")
        upload_path = Path(upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)

        student_name = data.student_name.strip().lower()
        student = await UserRepository.get_user_by_full_name(db, student_name)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
        # Normalize course_id to UUID
        if isinstance(course_id, UUID):
            course_uuid = course_id
        else:
            try:
                course_uuid = UUID(str(course_id))
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course_id format")
        course = await CourseRepository.get_course_by_id(db, course_uuid)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        #Check for existing submission
        existing = await AssignmentRepository.student_has_submitted(db, student.id, course_uuid)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already submitted this assignment"
            ) 
        #unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_location = upload_path / file.filename
        with open(file_location, "wb") as f:
            f.write(await file.read())

        assignment_dict = {
            "course_id": course.id,
            "student_id": student.id,
            "subject": data.subject,
            "description": data.description,
            "file_path": str(file_location),
            "original_filename": file.filename
        }

        assignment = await AssignmentRepository.create_assignment(db, assignment_dict)
        await db.commit()
        await db.refresh(assignment)
        return AssignmentResponse.model_validate(assignment)

    @staticmethod
    async def get_all_assignments(db: AsyncSession):
        assignments = await AssignmentRepository.get_all_assignments(db)
        return [AssignmentResponse.model_validate(a) for a in assignments]

    @staticmethod
    async def get_assignments_for_student(
        db: AsyncSession,
        student_name: str
    ):
        normalised_name = student_name.strip()
        student = await UserRepository.get_user_by_full_name(db, normalised_name)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
        assignments = await AssignmentRepository.get_assignments_by_student_id(db, student.id)
        return [AssignmentResponse.model_validate(a) for a in assignments]

