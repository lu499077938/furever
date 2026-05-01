from fastapi import APIRouter, Depends

from app.core.deps import get_current_user, get_interaction_repo, get_post_repo
from app.core.response import success
from app.repositories.base import InteractionRepository, PostRepository
from app.services import interaction_service

router = APIRouter(prefix="/posts", tags=["interactions"])


@router.post("/{post_id}/like")
async def toggle_like(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    interaction_repo: InteractionRepository = Depends(get_interaction_repo),
    post_repo: PostRepository = Depends(get_post_repo),
) -> dict:
    return success(interaction_service.toggle_like(interaction_repo, post_repo, post_id, current_user["id"]))


@router.post("/{post_id}/collect")
async def toggle_collect(
    post_id: int,
    current_user: dict = Depends(get_current_user),
    interaction_repo: InteractionRepository = Depends(get_interaction_repo),
    post_repo: PostRepository = Depends(get_post_repo),
) -> dict:
    return success(interaction_service.toggle_collect(interaction_repo, post_repo, post_id, current_user["id"]))
