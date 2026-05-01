from fastapi import APIRouter, Depends

from app.core.deps import get_user_repo
from app.core.response import success
from app.repositories.base import UserRepository
from app.schemas.auth import LoginReq, RegisterReq
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    payload: RegisterReq,
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    return success(auth_service.register(user_repo, payload.username, payload.password, payload.nickname))


@router.post("/login")
async def login(
    payload: LoginReq,
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    return success(auth_service.login(user_repo, payload.username, payload.password))
