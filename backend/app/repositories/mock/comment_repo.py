from app.repositories.base import CommentRepository
from app.repositories.mock.storage import DATA, next_id, now_ts, paginate


class MockCommentRepository(CommentRepository):
    def create_comment(self, payload: dict) -> dict:
        item = {
            "id": next_id("comments"),
            "post_id": payload["post_id"],
            "user_id": payload["user_id"],
            "content": payload["content"],
            "reply_to_comment_id": payload.get("reply_to_comment_id"),
            "is_edited": 0,
            "edited_at": None,
            "like_count": 0,
            "reply_count": 0,
            "created_at": now_ts(),
            "updated_at": now_ts(),
            "created_by": payload["user_id"],
            "updated_by": payload["user_id"],
            "is_deleted": 0,
        }
        DATA["comments"].append(item)
        
        if item["reply_to_comment_id"]:
            parent_comment = self.get_comment(item["reply_to_comment_id"])
            if parent_comment:
                parent_comment["reply_count"] = (parent_comment.get("reply_count") or 0) + 1
        
        return item

    def list_comments(self, post_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        comments = [c for c in DATA["comments"] if c["post_id"] == post_id and c["is_deleted"] == 0]
        comments.sort(key=lambda x: x["created_at"])
        return paginate(comments, page, page_size)

    def get_comment(self, comment_id: int) -> dict | None:
        for c in DATA["comments"]:
            if c["id"] == comment_id and c["is_deleted"] == 0:
                return c
        return None

    def update_comment(self, comment_id: int, user_id: int, content: str) -> dict | None:
        comment = self.get_comment(comment_id)
        if not comment or comment["user_id"] != user_id:
            return None
        comment["content"] = content
        comment["is_edited"] = 1
        comment["edited_at"] = now_ts()
        comment["updated_at"] = now_ts()
        comment["updated_by"] = user_id
        return comment

    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        comment = self.get_comment(comment_id)
        if not comment or comment["user_id"] != user_id:
            return False
        comment["is_deleted"] = 1
        comment["updated_at"] = now_ts()
        comment["updated_by"] = user_id
        return True

    def get_replies(self, comment_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        replies = [c for c in DATA["comments"] if c["reply_to_comment_id"] == comment_id and c["is_deleted"] == 0]
        replies.sort(key=lambda x: x["created_at"])
        return paginate(replies, page, page_size)

    def get_comment_depth(self, comment_id: int) -> int:
        depth = 1
        current_id = comment_id
        while True:
            comment = self.get_comment(current_id)
            if not comment or not comment.get("reply_to_comment_id"):
                break
            current_id = comment["reply_to_comment_id"]
            depth += 1
        return depth

    def list_root_comments(self, post_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        comments = [c for c in DATA["comments"] if c["post_id"] == post_id and c["reply_to_comment_id"] is None and c["is_deleted"] == 0]
        comments.sort(key=lambda x: x["created_at"])
        return paginate(comments, page, page_size)
