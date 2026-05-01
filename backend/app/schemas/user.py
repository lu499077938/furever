from pydantic import BaseModel, Field


class UpdateNicknameReq(BaseModel):
    nickname: str = Field(min_length=1, max_length=20)


class UpdatePasswordReq(BaseModel):
    old_password: str = Field(min_length=6, max_length=20)
    new_password: str = Field(min_length=6, max_length=20)


class UpdateAvatarReq(BaseModel):
    avatar: str = Field(min_length=1)


class UserProfileResp(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: str
