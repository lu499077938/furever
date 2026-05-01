from pydantic import BaseModel, Field

class FollowResp(BaseModel):
    active: bool = Field(..., description="是否已关注（true=已关注，false=未关注）")
    following_count: int = Field(..., description="目标用户当前的关注数")
    follower_count: int = Field(..., description="目标用户当前的粉丝数")
