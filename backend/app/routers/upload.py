from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from app.core.deps import get_current_user
from app.core.response import success
from app.services import upload_service
from app.utils.image import validate_upload_file

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    _user: dict = Depends(get_current_user),
) -> dict:
    content = await file.read()
    validate_upload_file(file, content)
    ext = Path(file.filename or "").suffix.lower()
    result = upload_service.save_image(content, ext)
    return success(result)
