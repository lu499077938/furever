from app.repositories.base import PostRepository
from app.repositories.mock.storage import DATA, now_ts, next_id, paginate


def _visible_posts() -> list[dict]:
    return [item for item in DATA["posts"] if item["is_deleted"] == 0]


class MockPostRepository(PostRepository):
    def create_post(self, payload: dict) -> dict:
        item = {
            "id": next_id("posts"),
            "user_id": payload["user_id"],
            "title": payload["title"],
            "content": payload["content"],
            "images": payload["images"],
            "cover_image": payload["images"][0],
            "cover_thumb_url": payload.get("thumb_images", payload["images"])[0],
            "like_count": 0,
            "collect_count": 0,
            "comment_count": 0,
            "created_at": now_ts(),
            "updated_at": now_ts(),
            "created_by": payload["user_id"],
            "updated_by": payload["user_id"],
            "is_deleted": 0,
        }
        DATA["posts"].append(item)
        return item

    def list_posts(self, page: int, page_size: int) -> tuple[int, list[dict]]:
        posts = sorted(_visible_posts(), key=lambda x: x["created_at"], reverse=True)
        return paginate(posts, page, page_size)

    def get_post(self, post_id: int) -> dict | None:
        return next((p for p in _visible_posts() if p["id"] == post_id), None)

    def delete_post(self, post_id: int, user_id: int) -> bool:
        post = self.get_post(post_id)
        if not post:
            return False
        if post["user_id"] != user_id:
            return False
        post["is_deleted"] = 1
        post["updated_by"] = user_id
        post["updated_at"] = now_ts()
        return True

    def search_posts(self, keyword: str, page: int, page_size: int) -> tuple[int, list[dict]]:
        posts = [
            p
            for p in _visible_posts()
            if keyword.lower() in p["title"].lower() or keyword.lower() in p["content"].lower()
        ]
        posts.sort(key=lambda x: x["created_at"], reverse=True)
        return paginate(posts, page, page_size)
