from fastapi import HTTPException

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.base import UserRepository


def register(user_repo: UserRepository, username: str, password: str, nickname: str) -> dict:
    exists = user_repo.get_by_username(username)
    if exists:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = user_repo.create_user(username=username, nickname=nickname, password_hash=hash_password(password))
    token = create_access_token(user["id"], user["password_version"])
    return {"token": token, "user": {"id": user["id"], "username": user["username"], "nickname": user["nickname"], "avatar": user["avatar"]}}


def login(user_repo: UserRepository, username: str, password: str) -> dict:
    user = user_repo.get_by_username(username)
    if not user or not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    token = create_access_token(user["id"], user["password_version"])
    return {"token": token, "user": {"id": user["id"], "username": user["username"], "nickname": user["nickname"], "avatar": user["avatar"]}}
