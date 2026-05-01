from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_current_user_optional, get_interaction_repo, get_post_repo, get_user_repo, get_follow_repo
from app.core.response import success
from app.repositories.base import InteractionRepository, PostRepository, UserRepository, FollowRepository
from app.schemas.post import PostCreateReq
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("")
async def create_post(
    payload: PostCreateReq,
    current_user: dict = Depends(get_current_user),
    post_repo: PostRepository = Depends(get_post_repo),
) -> dict:
    return success(post_service.create_post(post_repo, current_user["id"], payload.model_dump()))


@router.get("")
async def list_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    post_repo: PostRepository = Depends(get_post_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    return success(post_service.list_posts(post_repo, user_repo, page, page_size))


@router.get("/search")
async def search_posts(
    q: str = Query(min_length=1, max_length=50),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    post_repo: PostRepository = Depends(get_post_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    return success(post_service.search_posts(post_repo, user_repo, q, page, page_size))


@router.get("/{post_id}")
async def post_detail(
    post_id: int,
    current_user: dict | None = Depends(get_current_user_optional),
    post_repo: PostRepository = Depends(get_post_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    interaction_repo: InteractionRepository = Depends(get_interaction_repo),
    follow_repo: FollowRepository = Depends(get_follow_repo),
) -> dict:
    user_id = current_user["id"] if current_user else None
    return success(post_service.post_detail(post_repo, user_repo, interaction_repo, follow_repo, post_id, user_id))


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    post_repo: PostRepository = Depends(get_post_repo),
) -> dict:
    post_service.delete_post(post_repo, post_id, current_user["id"])
    return success(True)
