from app.repositories.base import NotificationRepository
from app.repositories.mock.storage import DATA, next_id, now_ts, paginate


class MockNotificationRepository(NotificationRepository):
    def create_notification(self, payload: dict) -> dict:
        item = {
            "id": next_id("notifications"),
            "user_id": payload["user_id"],
            "type": payload["type"],
            "content": payload["content"],
            "related_id": payload["related_id"],
            "is_read": False,
            "created_at": now_ts(),
            "updated_at": now_ts(),
            "created_by": 0,
            "updated_by": 0,
            "is_deleted": 0,
        }
        DATA["notifications"].append(item)
        return item

    def list_notifications(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        items = [n for n in DATA["notifications"] if n["user_id"] == user_id and n["is_deleted"] == 0]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return paginate(items, page, page_size)

    def unread_count(self, user_id: int) -> int:
        return len([n for n in DATA["notifications"] if n["user_id"] == user_id and n["is_deleted"] == 0 and not n["is_read"]])

    def read_all(self, user_id: int) -> int:
        updated = 0
        for item in DATA["notifications"]:
            if item["user_id"] != user_id or item["is_deleted"] != 0 or item["is_read"]:
                continue
            item["is_read"] = True
            item["updated_at"] = now_ts()
            item["updated_by"] = user_id
            updated += 1
        return updated

    def read_one(self, user_id: int, notification_id: int) -> bool:
        item = next((n for n in DATA["notifications"] if n["id"] == notification_id and n["user_id"] == user_id and n["is_deleted"] == 0), None)
        if not item:
            return False
        item["is_read"] = True
        item["updated_at"] = now_ts()
        item["updated_by"] = user_id
        return True
