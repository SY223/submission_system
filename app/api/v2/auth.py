from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db, auth_get_current_user
from app.services.auth_services import AuthService
from app.schemas.auth_schema import TokenResponse, LoginRequest, RegisterRequest, RefreshRequest
from app.schemas.user_schema import UserCreate, UserRead

auth_router_v2 = APIRouter()

@auth_router_v2.post("/register", response_model=UserRead)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await AuthService.register(db, data)

@auth_router_v2.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_async_db)
):
    return await AuthService.login(db, form_data.username, form_data.password)

@auth_router_v2.get("/me", response_model=UserRead)
async def get_me(
    current_user = Depends(auth_get_current_user)
):
    return UserRead.model_validate(current_user)

@auth_router_v2.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_async_db)
):
    return await AuthService.refresh(data, db)

@auth_router_v2.post("/logout")
async def logout(
    current_user = Depends(auth_get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    return await AuthService.logout(db, current_user)

