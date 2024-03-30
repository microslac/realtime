from .base import EnvSettings, Field


class DatabaseSettings(EnvSettings):
    host: str = Field(alias="DB_HOST")
    port: int = Field(alias="DB_PORT")
    username: str = Field(alias="DB_USERNAME")
    password: str = Field(alias="DB_PASSWORD")
    database: str = Field(alias="DB_DATABASE")
