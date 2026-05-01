from fastapi import HTTPException

from app.repositories.base import InteractionRepository, PostRepository


def toggle_like(interaction_repo: InteractionRepository, post_repo: PostRepository, post_id: int, user_id: int) -> dict:
    post = post_repo.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    result = interaction_repo.toggle_like(post_id, user_id)
    post["like_count"] = max(0, post["like_count"] + (1 if result["liked"] else -1))
    return {"active": result["liked"], "count": post["like_count"]}


def toggle_collect(interaction_repo: InteractionRepository, post_repo: PostRepository, post_id: int, user_id: int) -> dict:
    post = post_repo.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    result = interaction_repo.toggle_collect(post_id, user_id)
    post["collect_count"] = max(0, post["collect_count"] + (1 if result["collected"] else -1))
    return {"active": result["collected"], "count": post["collect_count"]}
