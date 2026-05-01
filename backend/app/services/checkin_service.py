from app.repositories.base import CheckinRepository


def checkin(checkin_repo: CheckinRepository, user_id: int) -> dict:
    return checkin_repo.checkin(user_id)


def checkin_status(checkin_repo: CheckinRepository, user_id: int) -> dict:
    return checkin_repo.get_checkin_status(user_id)
