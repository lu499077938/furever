from abc import ABC, abstractmethod
from typing import Any


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, username: str, nickname: str, password_hash: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def update_nickname(self, user_id: int, nickname: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_avatar(self, user_id: int, avatar_url: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_password(self, user_id: int, password_hash: str) -> dict[str, Any]:
        raise NotImplementedError


class PostRepository(ABC):
    @abstractmethod
    def create_post(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list_posts(self, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def get_post(self, post_id: int) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def delete_post(self, post_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def search_posts(self, keyword: str, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError


class CommentRepository(ABC):
    @abstractmethod
    def create_comment(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list_comments(self, post_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def get_comment(self, comment_id: int) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def update_comment(self, comment_id: int, user_id: int, content: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_replies(self, comment_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def get_comment_depth(self, comment_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def list_root_comments(self, post_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError


class CommentLikeRepository(ABC):
    @abstractmethod
    def toggle_like(self, comment_id: int, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def has_liked(self, comment_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_like_users(self, comment_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        raise NotImplementedError

    @abstractmethod
    def get_like_count(self, comment_id: int) -> int:
        raise NotImplementedError


class InteractionRepository(ABC):
    @abstractmethod
    def toggle_like(self, post_id: int, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def toggle_collect(self, post_id: int, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def has_liked(self, post_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def has_collected(self, post_id: int, user_id: int) -> bool:
        raise NotImplementedError


class CheckinRepository(ABC):
    @abstractmethod
    def checkin(self, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_checkin_status(self, user_id: int) -> dict[str, Any]:
        raise NotImplementedError


class NotificationRepository(ABC):
    @abstractmethod
    def create_notification(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list_notifications(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def unread_count(self, user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def read_all(self, user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def read_one(self, user_id: int, notification_id: int) -> bool:
        raise NotImplementedError


class ProfileRepository(ABC):
    @abstractmethod
    def list_my_posts(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def list_my_collects(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def list_my_likes(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError


class PointsRepository(ABC):
    @abstractmethod
    def get_points_overview(self, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list_points_logs(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        raise NotImplementedError


class FollowRepository(ABC):
    @abstractmethod
    def toggle_follow(self, follower_id: int, following_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def is_following(self, follower_id: int, following_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_following_count(self, user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_follower_count(self, user_id: int) -> int:
        raise NotImplementedError
