from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_notification_repo
from app.core.response import success
from app.repositories.base import NotificationRepository
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def list_notifications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    notification_repo: NotificationRepository = Depends(get_notification_repo),
) -> dict:
    return success(notification_service.list_notifications(notification_repo, current_user["id"], page, page_size))


@router.get("/unread-count")
async def unread_count(
    current_user: dict = Depends(get_current_user),
    notification_repo: NotificationRepository = Depends(get_notification_repo),
) -> dict:
    return success(notification_service.unread_count(notification_repo, current_user["id"]))


@router.put("/read-all")
async def read_all(
    current_user: dict = Depends(get_current_user),
    notification_repo: NotificationRepository = Depends(get_notification_repo),
) -> dict:
    return success(notification_service.read_all(notification_repo, current_user["id"]))


@router.put("/{notification_id}/read")
async def read_one(
    notification_id: int,
    current_user: dict = Depends(get_current_user),
    notification_repo: NotificationRepository = Depends(get_notification_repo),
) -> dict:
    return success(notification_service.read_one(notification_repo, current_user["id"], notification_id))
