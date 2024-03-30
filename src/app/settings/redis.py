from .base import EnvSettings, Field


class RedisSettings(EnvSettings):
    protocol: str = Field(alias="REDIS_PROTOCOL", default="redis")
    host: str = Field(alias="REDIS_HOST", default="localhost")
    port: int = Field(alias="REDIS_PORT", default=6379)
    database: int = Field(alias="REDIS_DATABASE", default=1)
    username: str = Field(alias="REDIS_USERNAME", default="")
    password: str = Field(alias="REDIS_PASSWORD", default="")

    @property
    def url(self):
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        return f"{self.protocol}://{self.host}:{self.port}/{self.database}"
