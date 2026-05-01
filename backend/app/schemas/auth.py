from pydantic import BaseModel, Field, field_validator


class RegisterReq(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=6, max_length=20)
    nickname: str = Field(min_length=1, max_length=20)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("用户名仅支持字母和数字")
        return value


class LoginReq(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=6, max_length=20)


class UserInfoResp(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: str


class TokenResp(BaseModel):
    token: str
    user: UserInfoResp
