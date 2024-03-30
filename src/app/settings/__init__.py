from .base import EnvSettings
from .database import DatabaseSettings
from .general import ApiSettings, CorsSettings
from .rabbit import RabbitSettings
from .websocket import WebsocketSettings
from .redis import RedisSettings

__all__ = ["settings"]


class Settings(EnvSettings):
    api: ApiSettings = ApiSettings()
    cors: CorsSettings = CorsSettings()
    db: DatabaseSettings = DatabaseSettings()
    rabbit: RabbitSettings = RabbitSettings()
    websocket: WebsocketSettings = WebsocketSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
