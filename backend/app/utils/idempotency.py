from datetime import datetime, timedelta
from typing import Any

_CACHE: dict[str, tuple[datetime, Any]] = {}


def get_cached_result(client_id: str) -> Any | None:
    data = _CACHE.get(client_id)
    if not data:
        return None
    created_at, payload = data
    if datetime.now() - created_at > timedelta(seconds=30):
        _CACHE.pop(client_id, None)
        return None
    return payload


def put_cached_result(client_id: str, payload: Any) -> None:
    _CACHE[client_id] = (datetime.now(), payload)
