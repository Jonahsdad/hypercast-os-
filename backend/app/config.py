from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


EnvType = Literal["dev", "prod", "test"]


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Hypercast OS API"
    app_env: EnvType = "dev"
    log_level: str = "INFO"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    cors_origins: list[str] = ["*"]

    # Future persistence (Postgres, etc.)
    database_url: AnyUrl | None = None

    class Config:
        env_prefix = ""


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
