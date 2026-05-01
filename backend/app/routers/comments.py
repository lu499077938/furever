from fastapi import APIRouter, Depends, Query

from app.core.deps import (
    get_comment_like_repo,
    get_comment_repo,
    get_current_user,
    get_current_user_optional,
    get_notification_repo,
    get_post_repo,
    get_user_repo,
)
from app.core.response import success
from app.repositories.base import (
    CommentLikeRepository,
    CommentRepository,
    NotificationRepository,
    PostRepository,
    UserRepository,
)
from app.schemas.comment import (
    CommentCreateReq,
    CommentReplyReq,
    CommentUpdateReq,
)
from app.services import comment_service

router = APIRouter(prefix="/posts", tags=["comments"])


@router.post("/{post_id}/comments")
async def create_comment(
    post_id: int,
    payload: CommentCreateReq,
    current_user: dict = Depends(get_current_user),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    post_repo: PostRepository = Depends(get_post_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    notification_repo: NotificationRepository = Depends(get_notification_repo),
) -> dict:
    result = comment_service.create_comment(
        comment_repo=comment_repo,
        post_repo=post_repo,
        user_repo=user_repo,
        notification_repo=notification_repo,
        user_id=current_user["id"],
        post_id=post_id,
        content=payload.content,
        client_id=payload.client_id,
    )
    return success(result)


@router.get("/{post_id}/comments")
async def list_comments(
    post_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    load_replies: bool = Query(default=False),
    current_user: dict | None = Depends(get_current_user_optional),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    comment_like_repo: CommentLikeRepository = Depends(get_comment_like_repo),
) -> dict:
    current_user_id = current_user["id"] if current_user else None
    return success(
        comment_service.list_comments(
            comment_repo,
            user_repo,
            comment_like_repo,
            post_id,
            page,
            page_size,
            current_user_id,
            load_replies,
        )
    )


@router.post("/{post_id}/comments/{comment_id}/reply")
async def reply_comment(
    post_id: int,
    comment_id: int,
    payload: CommentReplyReq,
    current_user: dict = Depends(get_current_user),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    post_repo: PostRepository = Depends(get_post_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    notification_repo: NotificationRepository = Depends(get_notification_repo),
) -> dict:
    result = comment_service.reply_comment(
        comment_repo=comment_repo,
        post_repo=post_repo,
        user_repo=user_repo,
        notification_repo=notification_repo,
        user_id=current_user["id"],
        post_id=post_id,
        comment_id=comment_id,
        content=payload.content,
        client_id=payload.client_id,
    )
    return success(result)


@router.put("/{post_id}/comments/{comment_id}")
async def update_comment(
    post_id: int,
    comment_id: int,
    payload: CommentUpdateReq,
    current_user: dict = Depends(get_current_user),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    result = comment_service.update_comment(
        comment_repo=comment_repo,
        user_repo=user_repo,
        comment_id=comment_id,
        user_id=current_user["id"],
        content=payload.content,
    )
    return success(result)


@router.delete("/{post_id}/comments/{comment_id}")
async def delete_comment(
    post_id: int,
    comment_id: int,
    current_user: dict = Depends(get_current_user),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    post_repo: PostRepository = Depends(get_post_repo),
) -> dict:
    comment_service.delete_comment(
        comment_repo=comment_repo,
        post_repo=post_repo,
        comment_id=comment_id,
        user_id=current_user["id"],
        post_id=post_id,
    )
    return success(None)


@router.get("/{post_id}/comments/{comment_id}/replies")
async def get_comment_replies(
    post_id: int,
    comment_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: dict | None = Depends(get_current_user_optional),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    comment_like_repo: CommentLikeRepository = Depends(get_comment_like_repo),
) -> dict:
    current_user_id = current_user["id"] if current_user else None
    return success(
        comment_service.get_replies(
            comment_repo,
            user_repo,
            comment_like_repo,
            comment_id,
            page,
            page_size,
            current_user_id,
        )
    )


@router.post("/{post_id}/comments/{comment_id}/like")
async def toggle_comment_like(
    post_id: int,
    comment_id: int,
    client_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    comment_like_repo: CommentLikeRepository = Depends(get_comment_like_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    notification_repo: NotificationRepository = Depends(get_notification_repo),
) -> dict:
    result = comment_service.toggle_comment_like(
        comment_repo=comment_repo,
        comment_like_repo=comment_like_repo,
        user_repo=user_repo,
        notification_repo=notification_repo,
        comment_id=comment_id,
        user_id=current_user["id"],
        client_id=client_id,
    )
    return success(result)


@router.get("/{post_id}/comments/{comment_id}/likes")
async def get_comment_like_users(
    post_id: int,
    comment_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=20),
    comment_like_repo: CommentLikeRepository = Depends(get_comment_like_repo),
) -> dict:
    return success(
        comment_service.get_comment_like_users(
            comment_like_repo,
            comment_id,
            page,
            page_size,
        )
    )
