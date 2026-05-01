from datetime import datetime

from pydantic import BaseModel, Field


class PostCreateReq(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)
    images: list[str] = Field(min_length=1, max_length=9)
    thumb_images: list[str] = Field(default_factory=list, max_length=9)
    client_id: str


class PostCardResp(BaseModel):
    id: int
    cover_thumb_url: str
    title: str
    author_nickname: str
    author_avatar: str
    like_count: int
    created_at: datetime


class PostDetailResp(BaseModel):
    id: int
    title: str
    content: str
    images: list[str]
    cover_thumb_url: str
    author_id: int
    author_nickname: str
    author_avatar: str
    like_count: int
    collect_count: int
    comment_count: int
    is_liked: bool
    is_collected: bool
    is_followed: bool
    created_at: datetime
