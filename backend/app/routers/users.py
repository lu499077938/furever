from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_profile_repo, get_user_repo
from app.core.response import success
from app.repositories.base import ProfileRepository, UserRepository
from app.schemas.user import UpdateAvatarReq, UpdateNicknameReq, UpdatePasswordReq
from app.services import profile_service, user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)) -> dict:
    return success(user_service.get_me(current_user))


@router.put("/me/nickname")
async def update_nickname(
    payload: UpdateNicknameReq,
    current_user: dict = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    return success(user_service.update_nickname(user_repo, current_user["id"], payload.nickname))


@router.put("/me/avatar")
async def update_avatar(
    payload: UpdateAvatarReq,
    current_user: dict = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    return success(user_service.update_avatar(user_repo, current_user["id"], payload.avatar))


@router.put("/me/password")
async def update_password(
    payload: UpdatePasswordReq,
    current_user: dict = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    return success(user_service.update_password(user_repo, current_user, payload.old_password, payload.new_password))


@router.get("/me/posts")
async def my_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    profile_repo: ProfileRepository = Depends(get_profile_repo),
) -> dict:
    return success(profile_service.my_posts(profile_repo, current_user["id"], page, page_size))


@router.get("/me/collects")
async def my_collects(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    profile_repo: ProfileRepository = Depends(get_profile_repo),
) -> dict:
    return success(profile_service.my_collects(profile_repo, current_user["id"], page, page_size))


@router.get("/me/likes")
async def my_likes(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    profile_repo: ProfileRepository = Depends(get_profile_repo),
) -> dict:
    return success(profile_service.my_likes(profile_repo, current_user["id"], page, page_size))
