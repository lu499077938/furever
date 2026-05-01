from fastapi import HTTPException
from app.repositories.base import FollowRepository, UserRepository
from app.schemas.follow import FollowResp

def toggle_follow(follower_id: int, following_id: int, follow_repo: FollowRepository, user_repo: UserRepository) -> FollowResp:
    if follower_id == following_id:
        raise HTTPException(status_code=400, detail={"code": 40001, "msg": "不能关注自己"})
    
    target_user = user_repo.get_by_id(following_id)
    if not target_user:
        raise HTTPException(status_code=404, detail={"code": 40401, "msg": "目标用户不存在"})
        
    follow_record = follow_repo.toggle_follow(follower_id, following_id)
    active = follow_record["is_deleted"] == 0
    
    following_count = follow_repo.get_following_count(following_id)
    follower_count = follow_repo.get_follower_count(following_id)
    
    return FollowResp(
        active=active,
        following_count=following_count,
        follower_count=follower_count
    )
