from datetime import datetime

from pydantic import BaseModel


class PointsResp(BaseModel):
    total_points: int
    checked_in_today: bool
    streak_days: int


class PointsLogResp(BaseModel):
    source: str
    amount: int
    remark: str
    created_at: datetime
