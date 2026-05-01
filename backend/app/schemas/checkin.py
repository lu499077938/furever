from pydantic import BaseModel


class FortuneResp(BaseModel):
    id: int
    level: str
    content: str
    day_index: int


class CheckinResp(BaseModel):
    checked_in_today: bool
    streak_days: int
    total_points: int
    points_earned: int = 0
    today_fortune: FortuneResp | None = None


class CheckinStatusResp(BaseModel):
    checked_in_today: bool
    streak_days: int
    total_points: int
    points_earned_today: int | None = None
    today_fortune: FortuneResp | None = None
