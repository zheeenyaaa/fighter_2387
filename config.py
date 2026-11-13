import os
from pathlib import Path
from typing import Literal
from pydantic import SecretStr
from sqlalchemy import URL

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    app_env: Literal["dev", "test", "prod"]
    feature_flag: bool
    db_host: str
    db_user: str
    db_password: SecretStr
    db_name: str



environment = os.getenv("ENVIRONMENT", "dev")
if environment not in {"dev", "test", "prod"}:
    raise ValueError(f"ENVIRONMENT должен быть dev, test или prod: {environment!r}")

env_file = Path(__file__).resolve().with_name(f".env.{environment}")
settings = Settings(_env_file=env_file)

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.db_user,
    password=settings.db_password.get_secret_value(),
    host=settings.db_host,
    port=5432,
    database=settings.db_name,
)