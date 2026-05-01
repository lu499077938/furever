from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PetGlow API"
    app_secret_key: str = "dev-secret-key"
    jwt_expire_days: int = 7
    database_url: str = "mysql+pymysql://user:pass@localhost:3306/furever"
    use_mock_db: bool = True
    upload_dir: str = "./uploads"
    static_base_url: str = "http://localhost:8000/static/uploads"
    cors_origins: list[str] = ["*"]

    @field_validator("upload_dir")
    @classmethod
    def normalize_upload_dir(cls, value: str) -> str:
        return str(Path(value))


@lru_cache
def get_settings() -> Settings:
    return Settings()
