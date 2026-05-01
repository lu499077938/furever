from app.repositories.base import PointsRepository
from app.repositories.mock.storage import DATA, paginate


class MockPointsRepository(PointsRepository):
    def get_points_overview(self, user_id: int) -> dict:
        points = next((p for p in DATA["points"] if p["user_id"] == user_id and p["is_deleted"] == 0), None)
        latest_checkin = any(c for c in DATA["checkins"] if c["user_id"] == user_id and c["is_deleted"] == 0)
        streak_days = 0
        if latest_checkin:
            user_checkins = [c for c in DATA["checkins"] if c["user_id"] == user_id and c["is_deleted"] == 0]
            streak_days = len(user_checkins)
        return {"total_points": points["total_points"] if points else 0, "checked_in_today": False, "streak_days": streak_days}

    def list_points_logs(self, user_id: int, page: int, page_size: int) -> tuple[int, list[dict]]:
        items = [item for item in DATA["points_logs"] if item["user_id"] == user_id and item["is_deleted"] == 0]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return paginate(items, page, page_size)
