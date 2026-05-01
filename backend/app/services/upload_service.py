from pathlib import Path

from app.core.config import get_settings
from app.utils.image import compress_image, create_thumbnail, generate_upload_name


def save_image(content: bytes, ext: str) -> dict:
    settings = get_settings()
    upload_root = Path(settings.upload_dir)
    original_dir = upload_root / "original"
    thumb_dir = upload_root / "thumb"
    original_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)

    compressed, output_ext = compress_image(content, ext)
    thumb, thumb_ext = create_thumbnail(content, ext)
    filename = generate_upload_name()
    original_name = f"{filename}{output_ext}"
    thumb_name = f"{filename}_thumb{thumb_ext}"

    (original_dir / original_name).write_bytes(compressed)
    (thumb_dir / thumb_name).write_bytes(thumb)

    base = settings.static_base_url.rstrip("/")
    return {"url": f"{base}/original/{original_name}", "thumb_url": f"{base}/thumb/{thumb_name}"}
