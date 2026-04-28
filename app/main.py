from fastapi import FastAPI
from app.api.v1.users import user_router
from app.api.v1.courses import course_router
from app.api.v1.assignments import assignment_router


app = FastAPI()

app.include_router(user_router, prefix="/api/v1/users", tags=["Teacher / Student Routes"])
app.include_router(course_router, prefix="/api/v1/courses", tags=["Courses Routes"])
app.include_router(assignment_router, prefix="/api/v1/assignments", tags=["Assignment Routes"])

app.get("/")
def root():
    return {
        "message": "A mini social assignment submission app!"
    }