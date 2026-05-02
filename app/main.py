from fastapi import FastAPI
from app.api.v1.users import user_router
from app.api.v1.courses import course_router
from app.api.v1.assignments import assignment_router
from app.api.v2.auth import auth_router_v2
from app.api.v2.users import user_router_v2
from app.api.v2.courses import course_router_v2
from app.api.v2.assignments import assignment_router_v2


app = FastAPI()

app.include_router(user_router, prefix="/api/v1/users", tags=["Teacher / Student Routes"])
app.include_router(course_router, prefix="/api/v1/courses", tags=["Courses Routes"])
app.include_router(assignment_router, prefix="/api/v1/assignments", tags=["Assignment Routes"])

app.include_router(auth_router_v2,  prefix='/api/v2/auth', tags=["Authentication Version 2"])
app.include_router(user_router_v2,  prefix='/api/v2/users', tags=["Teacher / Student Routes Version 2"])
app.include_router(course_router_v2,  prefix='/api/v2/courses', tags=["Courses Routes Version 2"])
app.include_router(assignment_router_v2,  prefix='/api/v2/assignments', tags=["Assignment Routes Version 2"])


app.get("/")
def root():
    return {
        "message": "A mini social assignment submission app!"
    }