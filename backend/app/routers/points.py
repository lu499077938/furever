from fastapi import APIRouter, Depends, Query

from app.core.deps import get_current_user, get_points_repo
from app.core.response import success
from app.repositories.base import PointsRepository
from app.services import points_service

router = APIRouter(prefix="/points", tags=["points"])


@router.get("")
async def overview(
    current_user: dict = Depends(get_current_user),
    points_repo: PointsRepository = Depends(get_points_repo),
) -> dict:
    return success(points_service.points_overview(points_repo, current_user["id"]))


@router.get("/logs")
async def logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    points_repo: PointsRepository = Depends(get_points_repo),
) -> dict:
    return success(points_service.points_logs(points_repo, current_user["id"], page, page_size))
