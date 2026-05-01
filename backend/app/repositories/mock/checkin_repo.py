import random
from datetime import timedelta

from app.repositories.base import CheckinRepository
from app.repositories.mock.storage import DATA, next_id, now_ts, today


def _choose_level() -> str:
    return random.choices(
        population=["上上签", "上签", "中上签", "中签"],
        weights=[10, 30, 35, 25],
        k=1,
    )[0]


def _pick_fortune(day_index: int) -> dict:
    level = _choose_level()
    candidates = [item for item in DATA["fortunes"] if item["level"] == level and item["day_index"] in (0, day_index)]
    if candidates:
        return random.choice(candidates)
    return random.choice(DATA["fortunes"])


def _current_streak(user_id: int) -> int:
    records = sorted([c for c in DATA["checkins"] if c["user_id"] == user_id and c["is_deleted"] == 0], key=lambda x: x["checkin_date"])
    if not records:
        return 0
    streak = 1
    for i in range(len(records) - 1, 0, -1):
        if records[i]["checkin_date"] - records[i - 1]["checkin_date"] == timedelta(days=1):
            streak += 1
            continue
        break
    return streak


def _add_points(user_id: int, amount: int, source: str, remark: str) -> None:
    point = next(item for item in DATA["points"] if item["user_id"] == user_id and item["is_deleted"] == 0)
    point["total_points"] += amount
    point["updated_at"] = now_ts()
    point["updated_by"] = user_id
    DATA["points_logs"].append(
        {
            "id": next_id("points_logs"),
            "user_id": user_id,
            "source": source,
            "amount": amount,
            "remark": remark,
            "created_at": now_ts(),
            "updated_at": now_ts(),
            "created_by": user_id,
            "updated_by": user_id,
            "is_deleted": 0,
        }
    )


class MockCheckinRepository(CheckinRepository):
    def checkin(self, user_id: int) -> dict:
        today_date = today()
        existing = next(
            (
                item
                for item in DATA["checkins"]
                if item["user_id"] == user_id and item["checkin_date"] == today_date and item["is_deleted"] == 0
            ),
            None,
        )
        if existing:
            return {"already": True, **self.get_checkin_status(user_id)}

        streak = _current_streak(user_id) + 1
        day_index = (streak - 1) % 7 + 1
        fortune = _pick_fortune(day_index)
        points_earned = random.randint(1, 10)
        if streak % 7 == 0:
            points_earned += 10
        elif streak % 3 == 0:
            points_earned += 5

        DATA["checkins"].append(
            {
                "id": next_id("checkins"),
                "user_id": user_id,
                "checkin_date": today_date,
                "fortune_id": fortune["id"],
                "points_earned": points_earned,
                "created_at": now_ts(),
                "updated_at": now_ts(),
                "created_by": user_id,
                "updated_by": user_id,
                "is_deleted": 0,
            }
        )
        _add_points(user_id, points_earned, "checkin", f"每日签到+{points_earned}")
        status = self.get_checkin_status(user_id)
        return {"already": False, "points_earned": points_earned, "fortune": status["today_fortune"], **status}

    def get_checkin_status(self, user_id: int) -> dict:
        today_date = today()
        records = [item for item in DATA["checkins"] if item["user_id"] == user_id and item["is_deleted"] == 0]
        today_record = next((item for item in records if item["checkin_date"] == today_date), None)
        streak = _current_streak(user_id)
        total_points = next(item["total_points"] for item in DATA["points"] if item["user_id"] == user_id and item["is_deleted"] == 0)
        today_fortune = None
        if today_record:
            today_fortune = next((item for item in DATA["fortunes"] if item["id"] == today_record["fortune_id"]), None)
        points_earned_today = today_record["points_earned"] if today_record else None
        return {
            "checked_in_today": today_record is not None,
            "streak_days": streak,
            "total_points": total_points,
            "points_earned_today": points_earned_today,
            "today_fortune": today_fortune,
        }
