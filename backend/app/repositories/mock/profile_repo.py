from app.repositories.base import ProfileRepository
from app.repositories.mock.storage import DATA, paginate


class MockProfileRepository(ProfileRepository):
    def list_my_posts(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        items = [p for p in DATA["posts"] if p["user_id"] == user_id and p["is_deleted"] == 0]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return paginate(items, page, page_size)

    def list_my_collects(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        post_ids = [c["post_id"] for c in DATA["collects"] if c["user_id"] == user_id and c["is_deleted"] == 0]
        items = [p for p in DATA["posts"] if p["id"] in post_ids and p["is_deleted"] == 0]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return paginate(items, page, page_size)

    def list_my_likes(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        post_ids = [c["post_id"] for c in DATA["likes"] if c["user_id"] == user_id and c["is_deleted"] == 0]
        items = [p for p in DATA["posts"] if p["id"] in post_ids and p["is_deleted"] == 0]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return paginate(items, page, page_size)
