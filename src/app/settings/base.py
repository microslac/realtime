import os
from pathlib import Path
from pydantic import Field  # noqa
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

environment = os.environ.get("APP_ENVIRONMENT", "")

env_file = ROOT_DIR / ".env"

env_files = (env_file,)

if environment in ("test", "dev", "stage", "prod"):
    environment_env_file = ROOT_DIR / f".env.{environment}"  # .env.prod
    if environment_env_file.exists():
        env_files = (env_file, environment_env_file)


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow", env_file=env_files, env_file_encoding="utf-8")
