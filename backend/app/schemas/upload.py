from pydantic import BaseModel


class UploadResp(BaseModel):
    url: str
    thumb_url: str
