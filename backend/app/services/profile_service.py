from app.repositories.base import ProfileRepository
from app.utils.pagination import normalize_page


def my_posts(profile_repo: ProfileRepository, user_id: int, page: int, page_size: int) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = profile_repo.list_my_posts(user_id, page, page_size)
    return {"total": total, "items": items}


def my_collects(profile_repo: ProfileRepository, user_id: int, page: int, page_size: int) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = profile_repo.list_my_collects(user_id, page, page_size)
    return {"total": total, "items": items}


def my_likes(profile_repo: ProfileRepository, user_id: int, page: int, page_size: int) -> dict:
    page, page_size = normalize_page(page, page_size)
    total, items = profile_repo.list_my_likes(user_id, page, page_size)
    return {"total": total, "items": items}
