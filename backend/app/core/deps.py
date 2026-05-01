from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.repositories.base import (
    CheckinRepository,
    CommentRepository,
    CommentLikeRepository,
    FollowRepository,
    InteractionRepository,
    NotificationRepository,
    PointsRepository,
    PostRepository,
    ProfileRepository,
    UserRepository,
)
from app.repositories.mock import (
    MockCheckinRepository,
    MockCommentRepository,
    MockCommentLikeRepository,
    MockFollowRepository,
    MockInteractionRepository,
    MockNotificationRepository,
    MockPointsRepository,
    MockPostRepository,
    MockProfileRepository,
    MockUserRepository,
)

bearer_scheme = HTTPBearer(auto_error=True)

_user_repo = MockUserRepository()
_post_repo = MockPostRepository()
_comment_repo = MockCommentRepository()
_comment_like_repo = MockCommentLikeRepository()
_interaction_repo = MockInteractionRepository()
_checkin_repo = MockCheckinRepository()
_notification_repo = MockNotificationRepository()
_profile_repo = MockProfileRepository()
_points_repo = MockPointsRepository()
_follow_repo = MockFollowRepository()


def _ensure_repo_mode() -> None:
    settings = get_settings()
    if settings.use_mock_db:
        return
    raise HTTPException(status_code=500, detail="当前环境未接入真实数据库实现")


def get_user_repo() -> UserRepository:
    _ensure_repo_mode()
    return _user_repo


def get_post_repo() -> PostRepository:
    _ensure_repo_mode()
    return _post_repo


def get_comment_repo() -> CommentRepository:
    _ensure_repo_mode()
    return _comment_repo


def get_comment_like_repo() -> CommentLikeRepository:
    _ensure_repo_mode()
    return _comment_like_repo


def get_interaction_repo() -> InteractionRepository:
    _ensure_repo_mode()
    return _interaction_repo


def get_checkin_repo() -> CheckinRepository:
    _ensure_repo_mode()
    return _checkin_repo


def get_notification_repo() -> NotificationRepository:
    _ensure_repo_mode()
    return _notification_repo


def get_profile_repo() -> ProfileRepository:
    _ensure_repo_mode()
    return _profile_repo


def get_points_repo() -> PointsRepository:
    _ensure_repo_mode()
    return _points_repo


def get_follow_repo() -> FollowRepository:
    _ensure_repo_mode()
    return _follow_repo


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict:
    payload = decode_access_token(credentials.credentials)
    user_id_raw = payload.get("sub")
    password_version = payload.get("pv", 1)
    if not user_id_raw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的登录信息")
    user = user_repo.get_by_id(int(user_id_raw))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")
    if user["password_version"] != password_version:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录已过期，请重新登录")
    return user

bearer_scheme_optional = HTTPBearer(auto_error=False)

def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme_optional),
    user_repo: UserRepository = Depends(get_user_repo),
) -> dict | None:
    if not credentials:
        return None
    try:
        payload = decode_access_token(credentials.credentials)
        user_id_raw = payload.get("sub")
        password_version = payload.get("pv", 1)
        if not user_id_raw:
            return None
        user = user_repo.get_by_id(int(user_id_raw))
        if not user or user["password_version"] != password_version:
            return None
        return user
    except Exception:
        return None
