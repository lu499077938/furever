from app.repositories.base import UserRepository
from app.repositories.mock.storage import DATA, now_ts, next_id


class MockUserRepository(UserRepository):
    def create_user(self, username: str, nickname: str, password_hash: str) -> dict:
        item = {
            "id": next_id("users"),
            "username": username,
            "nickname": nickname,
            "password_hash": password_hash,
            "avatar": "https://placehold.co/80x80",
            "password_version": 1,
            "created_at": now_ts(),
            "updated_at": now_ts(),
            "created_by": 0,
            "updated_by": 0,
            "is_deleted": 0,
        }
        DATA["users"].append(item)
        DATA["points"].append(
            {
                "id": item["id"],
                "user_id": item["id"],
                "total_points": 0,
                "created_at": now_ts(),
                "updated_at": now_ts(),
                "created_by": item["id"],
                "updated_by": item["id"],
                "is_deleted": 0,
            }
        )
        return item

    def get_by_username(self, username: str) -> dict | None:
        return next((u for u in DATA["users"] if u["username"] == username and u["is_deleted"] == 0), None)

    def get_by_id(self, user_id: int) -> dict | None:
        return next((u for u in DATA["users"] if u["id"] == user_id and u["is_deleted"] == 0), None)

    def update_nickname(self, user_id: int, nickname: str) -> dict:
        user = self.get_by_id(user_id)
        user["nickname"] = nickname
        user["updated_at"] = now_ts()
        user["updated_by"] = user_id
        return user

    def update_avatar(self, user_id: int, avatar_url: str) -> dict:
        user = self.get_by_id(user_id)
        user["avatar"] = avatar_url
        user["updated_at"] = now_ts()
        user["updated_by"] = user_id
        return user

    def update_password(self, user_id: int, password_hash: str) -> dict:
        user = self.get_by_id(user_id)
        user["password_hash"] = password_hash
        user["password_version"] += 1
        user["updated_at"] = now_ts()
        user["updated_by"] = user_id
        return user
