from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResp(GenericModel, Generic[T]):
    code: int = 0
    msg: str = "ok"
    data: T | None = None


class PageResp(BaseModel, Generic[T]):
    total: int = Field(default=0)
    items: list[T] = Field(default_factory=list)
