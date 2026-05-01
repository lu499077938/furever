from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentCreateReq(BaseModel):
    content: str = Field(min_length=1, max_length=200)
    client_id: str


class CommentReplyReq(BaseModel):
    content: str = Field(min_length=1, max_length=200)
    client_id: str


class CommentUpdateReq(BaseModel):
    content: str = Field(min_length=1, max_length=200)


class CommentResp(BaseModel):
    id: int
    content: str
    user_id: int
    user_nickname: str
    user_avatar: str
    reply_to_comment_id: Optional[int] = None
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    like_count: int = 0
    reply_count: int = 0
    created_at: datetime
    is_liked: bool = False
    replies: Optional[list["CommentResp"]] = None


CommentResp.model_rebuild()


class CommentLikeResp(BaseModel):
    liked: bool
    like_count: int


class CommentListResp(BaseModel):
    total: int
    items: list[CommentResp]
