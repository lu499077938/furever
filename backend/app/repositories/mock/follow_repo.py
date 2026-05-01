from typing import Any
from app.repositories.base import FollowRepository
from app.repositories.mock.storage import DATA, next_id, now_ts

class MockFollowRepository(FollowRepository):
    def toggle_follow(self, follower_id: int, following_id: int) -> dict[str, Any]:
        follows = DATA["follows"]
        for f in follows:
            if f["follower_id"] == follower_id and f["following_id"] == following_id:
                # toggle is_deleted
                f["is_deleted"] = 0 if f["is_deleted"] == 1 else 1
                f["updated_at"] = now_ts()
                f["updated_by"] = follower_id
                return f

        new_follow = {
            "id": next_id("follows"),
            "follower_id": follower_id,
            "following_id": following_id,
            "created_at": now_ts(),
            "updated_at": now_ts(),
            "created_by": follower_id,
            "updated_by": follower_id,
            "is_deleted": 0,
        }
        follows.append(new_follow)
        return new_follow

    def is_following(self, follower_id: int, following_id: int) -> bool:
        for f in DATA["follows"]:
            if f["follower_id"] == follower_id and f["following_id"] == following_id and f["is_deleted"] == 0:
                return True
        return False

    def get_following_count(self, user_id: int) -> int:
        return sum(1 for f in DATA["follows"] if f["follower_id"] == user_id and f["is_deleted"] == 0)

    def get_follower_count(self, user_id: int) -> int:
        return sum(1 for f in DATA["follows"] if f["following_id"] == user_id and f["is_deleted"] == 0)
