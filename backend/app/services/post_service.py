from fastapi import HTTPException

from app.repositories.base import InteractionRepository, PostRepository, UserRepository
from app.utils.idempotency import get_cached_result, put_cached_result
from app.utils.pagination import normalize_page


def _to_card(item: dict, user_repo: UserRepository) -> dict:
    author = user_repo.get_by_id(item["user_id"])
    return {
        "id": item["id"],
        "cover_thumb_url": item["cover_thumb_url"],
        "title": item["title"],
        "author_nickname": author["nickname"] if author else "",
        "author_avatar": author["avatar"] if author else "",
        "like_count": item["like_count"],
        "created_at": item["created_at"],
    }


def create_post(post_repo: PostRepository, user_id: int, payload: dict) -> dict:
    cached = get_cached_result(payload["client_id"])
    if cached:
        return cached
    if len(payload["images"]) > 9:
        raise HTTPException(status_code=400, detail="最多上传9张图片")
    created = post_repo.create_post(
        {
            "user_id": user_id,
            "title": payload["title"],
            "content": payload["content"],
            "images": payload["images"],
            "thumb_images": payload.get("thumb_images", []),
        }
    )
    result = {"id": created["id"]}
    put_cached_result(payload["client_id"], result)
    return result


def list_posts(post_repo: PostRepository, user_repo: UserRepository, page: int, page_size: int) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = post_repo.list_posts(page, page_size)
    return {"total": total, "items": [_to_card(item, user_repo) for item in items]}


def post_detail(
    post_repo: PostRepository,
    user_repo: UserRepository,
    interaction_repo: InteractionRepository,
    follow_repo: FollowRepository,
    post_id: int,
    user_id: int | None,
) -> dict:
    item = post_repo.get_post(post_id)
    if not item:
        raise HTTPException(status_code=404, detail="帖子不存在")
    author = user_repo.get_by_id(item["user_id"])
    
    is_liked = interaction_repo.has_liked(post_id, user_id) if user_id else False
    is_collected = interaction_repo.has_collected(post_id, user_id) if user_id else False
    is_followed = follow_repo.is_following(user_id, item["user_id"]) if user_id else False

    return {
        "id": item["id"],
        "title": item["title"],
        "content": item["content"],
        "images": item["images"],
        "cover_thumb_url": item["cover_thumb_url"],
        "author_id": item["user_id"],
        "author_nickname": author["nickname"] if author else "",
        "author_avatar": author["avatar"] if author else "",
        "like_count": item["like_count"],
        "collect_count": item["collect_count"],
        "comment_count": item["comment_count"],
        "is_liked": is_liked,
        "is_collected": is_collected,
        "is_followed": is_followed,
        "created_at": item["created_at"],
    }


def delete_post(post_repo: PostRepository, post_id: int, user_id: int) -> None:
    success = post_repo.delete_post(post_id, user_id)
    if success:
        return
    post = post_repo.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    raise HTTPException(status_code=403, detail="仅作者可删除")


def search_posts(post_repo: PostRepository, user_repo: UserRepository, keyword: str, page: int, page_size: int) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = post_repo.search_posts(keyword, page, page_size)
    return {"total": total, "items": [_to_card(item, user_repo) for item in items]}
