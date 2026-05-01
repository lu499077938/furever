from datetime import date, datetime

from app.repositories.mock import mock_data

DATA = mock_data.snapshot()


def now_ts() -> datetime:
    return datetime.now()


def today() -> date:
    return date.today()


def next_id(name: str) -> int:
    current = mock_data.ID_COUNTER[name]
    mock_data.ID_COUNTER[name] = current + 1
    return current


def paginate(items: list[dict], page: int, page_size: int) -> tuple[int, list[dict]]:
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return total, items[start:end]
