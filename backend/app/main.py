from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.routers import (
    auth,
    checkin,
    comments,
    follow,
    health,
    interactions,
    notifications,
    points,
    posts,
    upload,
    users,
)


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name)
    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health.router, prefix="/api/v1")
    application.include_router(auth.router, prefix="/api/v1")
    application.include_router(users.router, prefix="/api/v1")
    application.include_router(follow.router, prefix="/api/v1")
    application.include_router(upload.router, prefix="/api/v1")
    application.include_router(posts.router, prefix="/api/v1")
    application.include_router(interactions.router, prefix="/api/v1")
    application.include_router(comments.router, prefix="/api/v1")
    application.include_router(notifications.router, prefix="/api/v1")
    application.include_router(checkin.router, prefix="/api/v1")
    application.include_router(points.router, prefix="/api/v1")
    return application


app = create_app()
