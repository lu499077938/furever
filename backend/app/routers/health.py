from fastapi import APIRouter

from app.core.config import get_settings
from app.core.response import success

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    settings = get_settings()
    return success({"status": "ok", "service": settings.app_name})
