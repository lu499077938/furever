from typing import Any


def success(data: Any = None, msg: str = "ok") -> dict[str, Any]:
    return {"code": 0, "msg": msg, "data": data}


def fail(msg: str, code: int = 1, data: Any = None) -> dict[str, Any]:
    return {"code": code, "msg": msg, "data": data}
