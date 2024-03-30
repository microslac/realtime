from .base import EnvSettings, Field


class ApiSettings(EnvSettings):
    host: str = Field(alias="API_HOST", default="0.0.0.0")
    port: int = Field(alias="API_PORT", default=8016)


class CorsSettings(EnvSettings):
    allow_origins: list[str] = Field(alias="CORS_ALLOW_ORIGINS", default=["*"])
    allow_headers: list[str] = Field(alias="CORS_ALLOW_HEADERS", default=["*"])
    allow_credentials: bool = Field(alias="CORS_ALLOW_CREDENTIALS", default=True)
