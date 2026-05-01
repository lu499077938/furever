from fastapi import HTTPException

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.base import UserRepository


def get_me(user: dict) -> dict:
    return {"id": user["id"], "username": user["username"], "nickname": user["nickname"], "avatar": user["avatar"]}


def update_nickname(user_repo: UserRepository, user_id: int, nickname: str) -> dict:
    user = user_repo.update_nickname(user_id, nickname)
    return get_me(user)


def update_avatar(user_repo: UserRepository, user_id: int, avatar_url: str) -> dict:
    user = user_repo.update_avatar(user_id, avatar_url)
    return get_me(user)


def update_password(user_repo: UserRepository, user: dict, old_password: str, new_password: str) -> dict:
    if not verify_password(old_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="原密码错误")
    updated = user_repo.update_password(user["id"], hash_password(new_password))
    token = create_access_token(updated["id"], updated["password_version"])
    return {"token": token}
