from app.repositories.base import InteractionRepository
from app.repositories.mock.storage import DATA, next_id, now_ts


def _toggle(items: list[dict], key: str, post_id: int, user_id: int) -> bool:
    exists = next((item for item in items if item["post_id"] == post_id and item["user_id"] == user_id and item["is_deleted"] == 0), None)
    if exists:
        exists["is_deleted"] = 1
        exists["updated_at"] = now_ts()
        exists["updated_by"] = user_id
        return False
    items.append(
        {
            "id": next_id(key),
            "post_id": post_id,
            "user_id": user_id,
            "created_at": now_ts(),
            "updated_at": now_ts(),
            "created_by": user_id,
            "updated_by": user_id,
            "is_deleted": 0,
        }
    )
    return True


class MockInteractionRepository(InteractionRepository):
    def toggle_like(self, post_id: int, user_id: int) -> dict:
        liked = _toggle(DATA["likes"], "likes", post_id, user_id)
        return {"liked": liked}

    def toggle_collect(self, post_id: int, user_id: int) -> dict:
        collected = _toggle(DATA["collects"], "collects", post_id, user_id)
        return {"collected": collected}

    def has_liked(self, post_id: int, user_id: int) -> bool:
        return any(item for item in DATA["likes"] if item["post_id"] == post_id and item["user_id"] == user_id and item["is_deleted"] == 0)

    def has_collected(self, post_id: int, user_id: int) -> bool:
        return any(item for item in DATA["collects"] if item["post_id"] == post_id and item["user_id"] == user_id and item["is_deleted"] == 0)
