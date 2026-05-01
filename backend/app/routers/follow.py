from fastapi import APIRouter, Depends
from app.core.deps import get_current_user, get_follow_repo, get_user_repo
from app.core.response import success
from app.repositories.base import FollowRepository, UserRepository
from app.services import follow_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/{target_user_id}/follow")
async def toggle_follow(
    target_user_id: int,
    current_user: dict = Depends(get_current_user),
    follow_repo: FollowRepository = Depends(get_follow_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    result = follow_service.toggle_follow(
        follower_id=current_user["id"],
        following_id=target_user_id,
        follow_repo=follow_repo,
        user_repo=user_repo,
    )
    return success(result.model_dump())
