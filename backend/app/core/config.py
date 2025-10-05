from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Seedr"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    redis_url: str = "redis://localhost:6379/0"
    scheduler_timezone: str = "UTC"
    reminder_lead_minutes: int = 60


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
