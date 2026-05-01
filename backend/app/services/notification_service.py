from app.repositories.base import NotificationRepository
from app.utils.pagination import normalize_page


def list_notifications(notification_repo: NotificationRepository, user_id: int, page: int, page_size: int) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = notification_repo.list_notifications(user_id, page, page_size)
    return {"total": total, "items": items}


def unread_count(notification_repo: NotificationRepository, user_id: int) -> dict:
    return {"unread_count": notification_repo.unread_count(user_id)}


def read_all(notification_repo: NotificationRepository, user_id: int) -> dict:
    return {"updated": notification_repo.read_all(user_id)}


def read_one(notification_repo: NotificationRepository, user_id: int, notification_id: int) -> dict:
    updated = notification_repo.read_one(user_id, notification_id)
    return {"updated": updated}
