from app.repositories.base import PointsRepository
from app.utils.pagination import normalize_page


def points_overview(points_repo: PointsRepository, user_id: int) -> dict:
    return points_repo.get_points_overview(user_id)


def points_logs(points_repo: PointsRepository, user_id: int, page: int, page_size: int) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = points_repo.list_points_logs(user_id, page, page_size)
    return {"total": total, "items": items}
