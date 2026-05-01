from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from PIL import Image

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 10 * 1024 * 1024


def validate_upload_file(file: UploadFile, content: bytes) -> None:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTS or (file.content_type or "").lower() not in ALLOWED_MIME:
        raise HTTPException(status_code=400, detail="仅支持 jpg/png/webp 格式")
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="图片大小不能超过 10MB")


def _to_jpg_if_needed(image: Image.Image, original_ext: str) -> tuple[Image.Image, str]:
    if original_ext in (".jpg", ".jpeg", ".webp"):
        return image, original_ext
    if image.mode in ("RGBA", "LA"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        return background, ".jpg"
    return image.convert("RGB"), ".jpg"


def compress_image(content: bytes, ext: str) -> tuple[bytes, str]:
    image = Image.open(BytesIO(content))
    image, output_ext = _to_jpg_if_needed(image, ext)
    max_edge = max(image.size)
    if max_edge > 1920:
        ratio = 1920 / max_edge
        image = image.resize((int(image.width * ratio), int(image.height * ratio)))
    out = BytesIO()
    if output_ext == ".webp":
        image.save(out, format="WEBP", quality=85)
    elif output_ext == ".png":
        image.save(out, format="PNG", optimize=True)
    else:
        image.save(out, format="JPEG", quality=85, optimize=True)
    return out.getvalue(), output_ext


def create_thumbnail(content: bytes, ext: str) -> tuple[bytes, str]:
    image = Image.open(BytesIO(content))
    image, output_ext = _to_jpg_if_needed(image, ext)
    max_edge = max(image.size)
    if max_edge > 400:
        ratio = 400 / max_edge
        image = image.resize((int(image.width * ratio), int(image.height * ratio)))
    out = BytesIO()
    if output_ext == ".webp":
        image.save(out, format="WEBP", quality=80)
    elif output_ext == ".png":
        image.save(out, format="PNG", optimize=True)
    else:
        image.save(out, format="JPEG", quality=80, optimize=True)
    return out.getvalue(), output_ext


def generate_upload_name() -> str:
    return uuid4().hex
