from fastapi import HTTPException

from app.repositories.base import (
    CommentRepository,
    CommentLikeRepository,
    NotificationRepository,
    PostRepository,
    UserRepository,
)
from app.utils.idempotency import get_cached_result, put_cached_result
from app.utils.pagination import normalize_page


def _build_comment_resp(
    comment: dict,
    user_repo: UserRepository,
    comment_like_repo: CommentLikeRepository,
    current_user_id: int | None = None,
    load_replies: bool = False,
    comment_repo: CommentRepository | None = None,
) -> dict:
    user = user_repo.get_by_id(comment["user_id"])
    is_liked = False
    if current_user_id and comment_like_repo:
        is_liked = comment_like_repo.has_liked(comment["id"], current_user_id)
    
    replies = None
    if load_replies and comment_repo:
        total, reply_rows = comment_repo.get_replies(comment["id"], 1, 20)
        replies = [
            _build_comment_resp(
                r, user_repo, comment_like_repo, current_user_id, False, comment_repo
            )
            for r in reply_rows
        ]
    
    return {
        "id": comment["id"],
        "content": comment["content"],
        "user_id": comment["user_id"],
        "user_nickname": user["nickname"] if user else "",
        "user_avatar": user["avatar"] if user else "",
        "reply_to_comment_id": comment.get("reply_to_comment_id"),
        "is_edited": bool(comment.get("is_edited", 0)),
        "edited_at": comment.get("edited_at"),
        "like_count": comment.get("like_count", 0),
        "reply_count": comment.get("reply_count", 0),
        "created_at": comment["created_at"],
        "is_liked": is_liked,
        "replies": replies,
    }


def create_comment(
    comment_repo: CommentRepository,
    post_repo: PostRepository,
    user_repo: UserRepository,
    notification_repo: NotificationRepository,
    user_id: int,
    post_id: int,
    content: str,
    client_id: str,
) -> dict:
    cached = get_cached_result(client_id)
    if cached:
        return cached
    post = post_repo.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    comment = comment_repo.create_comment({"post_id": post_id, "user_id": user_id, "content": content})
    post["comment_count"] += 1
    if post["user_id"] != user_id:
        commenter = user_repo.get_by_id(user_id)
        notification_repo.create_notification(
            {
                "user_id": post["user_id"],
                "type": "comment",
                "content": f"{commenter['nickname']} 评论了你的帖子：{content[:20]}",
                "related_id": post_id,
            }
        )
    result = _build_comment_resp(comment, user_repo, None)
    put_cached_result(client_id, result)
    return result


def reply_comment(
    comment_repo: CommentRepository,
    post_repo: PostRepository,
    user_repo: UserRepository,
    notification_repo: NotificationRepository,
    user_id: int,
    post_id: int,
    comment_id: int,
    content: str,
    client_id: str,
) -> dict:
    cached = get_cached_result(client_id)
    if cached:
        return cached
    
    post = post_repo.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    
    parent_comment = comment_repo.get_comment(comment_id)
    if not parent_comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    depth = comment_repo.get_comment_depth(comment_id)
    if depth >= 3:
        raise HTTPException(status_code=400, detail="已达最大回复层级")
    
    comment = comment_repo.create_comment({
        "post_id": post_id,
        "user_id": user_id,
        "content": content,
        "reply_to_comment_id": comment_id,
    })
    post["comment_count"] += 1
    
    if parent_comment["user_id"] != user_id:
        commenter = user_repo.get_by_id(user_id)
        notification_repo.create_notification(
            {
                "user_id": parent_comment["user_id"],
                "type": "comment_reply",
                "content": f"{commenter['nickname']} 回复了你的评论：{content[:20]}",
                "related_id": post_id,
            }
        )
    
    result = _build_comment_resp(comment, user_repo, None)
    put_cached_result(client_id, result)
    return result


def update_comment(
    comment_repo: CommentRepository,
    user_repo: UserRepository,
    comment_id: int,
    user_id: int,
    content: str,
) -> dict:
    comment = comment_repo.update_comment(comment_id, user_id, content)
    if not comment:
        raise HTTPException(status_code=403, detail="无权编辑该评论")
    return _build_comment_resp(comment, user_repo, None)


def delete_comment(
    comment_repo: CommentRepository,
    post_repo: PostRepository,
    comment_id: int,
    user_id: int,
    post_id: int,
) -> bool:
    success = comment_repo.delete_comment(comment_id, user_id)
    if not success:
        raise HTTPException(status_code=403, detail="无权删除该评论")
    post = post_repo.get_post(post_id)
    if post and post["comment_count"] > 0:
        post["comment_count"] -= 1
    return True


def list_comments(
    comment_repo: CommentRepository,
    user_repo: UserRepository,
    comment_like_repo: CommentLikeRepository,
    post_id: int,
    page: int,
    page_size: int,
    current_user_id: int | None = None,
    load_replies: bool = False,
) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, rows = comment_repo.list_root_comments(post_id, page, page_size)
    items = []
    for row in rows:
        items.append(
            _build_comment_resp(
                row, user_repo, comment_like_repo, current_user_id, load_replies, comment_repo
            )
        )
    return {"total": total, "items": items}


def get_replies(
    comment_repo: CommentRepository,
    user_repo: UserRepository,
    comment_like_repo: CommentLikeRepository,
    comment_id: int,
    page: int,
    page_size: int,
    current_user_id: int | None = None,
) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, rows = comment_repo.get_replies(comment_id, page, page_size)
    items = []
    for row in rows:
        items.append(
            _build_comment_resp(row, user_repo, comment_like_repo, current_user_id, False, comment_repo)
        )
    return {"total": total, "items": items}


def toggle_comment_like(
    comment_repo: CommentRepository,
    comment_like_repo: CommentLikeRepository,
    user_repo: UserRepository,
    notification_repo: NotificationRepository,
    comment_id: int,
    user_id: int,
    client_id: str,
) -> dict:
    cached = get_cached_result(client_id)
    if cached:
        return cached
    
    comment = comment_repo.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    result = comment_like_repo.toggle_like(comment_id, user_id)
    
    if result["liked"] and comment["user_id"] != user_id:
        liker = user_repo.get_by_id(user_id)
        notification_repo.create_notification(
            {
                "user_id": comment["user_id"],
                "type": "comment_like",
                "content": f"{liker['nickname']} 赞了你的评论",
                "related_id": comment["post_id"],
            }
        )
    
    like_count = comment.get("like_count", 0)
    resp = {"liked": result["liked"], "like_count": like_count}
    put_cached_result(client_id, resp)
    return resp


def get_comment_like_users(
    comment_like_repo: CommentLikeRepository,
    comment_id: int,
    page: int,
    page_size: int,
) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = comment_like_repo.get_like_users(comment_id, page, page_size)
    return {"total": total, "items": items}
