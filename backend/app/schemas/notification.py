from datetime import datetime

from pydantic import BaseModel


class NotificationResp(BaseModel):
    id: int
    type: str
    content: str
    related_id: int
    is_read: bool
    created_at: datetime


class UnreadCountResp(BaseModel):
    unread_count: int
