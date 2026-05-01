from pydantic import BaseModel


class ToggleResp(BaseModel):
    active: bool
    count: int
