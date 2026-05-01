from app.repositories.mock.storage import DATA, next_id, now_ts, paginate


class MockCommentLikeRepository:
    def toggle_like(self, comment_id: int, user_id: int) -> dict:
        exists = next(
            (item for item in DATA["comment_likes"] if item["comment_id"] == comment_id and item["user_id"] == user_id and item["is_deleted"] == 0),
            None,
        )
        liked = False
        if exists:
            exists["is_deleted"] = 1
            exists["updated_at"] = now_ts()
            exists["updated_by"] = user_id
            liked = False
        else:
            DATA["comment_likes"].append(
                {
                    "id": next_id("comment_likes"),
                    "comment_id": comment_id,
                    "user_id": user_id,
                    "created_at": now_ts(),
                    "updated_at": now_ts(),
                    "created_by": user_id,
                    "updated_by": user_id,
                    "is_deleted": 0,
                }
            )
            liked = True
        
        comment = next((c for c in DATA["comments"] if c["id"] == comment_id and c["is_deleted"] == 0), None)
        if comment:
            current_count = comment.get("like_count", 0)
            comment["like_count"] = current_count + 1 if liked else max(0, current_count - 1)
        
        return {"liked": liked}

    def has_liked(self, comment_id: int, user_id: int) -> bool:
        return any(
            item for item in DATA["comment_likes"] 
            if item["comment_id"] == comment_id and item["user_id"] == user_id and item["is_deleted"] == 0
        )

    def get_like_users(self, comment_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        likes = [
            item for item in DATA["comment_likes"] 
            if item["comment_id"] == comment_id and item["is_deleted"] == 0
        ]
        likes.sort(key=lambda x: x["created_at"], reverse=True)
        user_ids = [like["user_id"] for like in likes]
        users = [u for u in DATA["users"] if u["id"] in user_ids]
        user_map = {u["id"]: u for u in users}
        items = []
        for like in likes:
            user = user_map.get(like["user_id"])
            if user:
                items.append({
                    "user_id": user["id"],
                    "nickname": user["nickname"],
                    "avatar": user["avatar"],
                })
        return paginate(items, page, page_size)

    def get_like_count(self, comment_id: int) -> int:
        return sum(
            1 for item in DATA["comment_likes"] 
            if item["comment_id"] == comment_id and item["is_deleted"] == 0
        )
