from fastapi import APIRouter, Depends

from app.core.deps import get_checkin_repo, get_current_user
from app.core.response import success
from app.repositories.base import CheckinRepository
from app.services import checkin_service

router = APIRouter(prefix="/checkin", tags=["checkin"])


@router.post("")
async def do_checkin(
    current_user: dict = Depends(get_current_user),
    checkin_repo: CheckinRepository = Depends(get_checkin_repo),
) -> dict:
    return success(checkin_service.checkin(checkin_repo, current_user["id"]))


@router.get("/status")
async def checkin_status(
    current_user: dict = Depends(get_current_user),
    checkin_repo: CheckinRepository = Depends(get_checkin_repo),
) -> dict:
    return success(checkin_service.checkin_status(checkin_repo, current_user["id"]))
