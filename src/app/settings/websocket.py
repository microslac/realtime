from typing import Optional
from .base import EnvSettings, Field


class WebsocketSettings(EnvSettings):
    url: str = Field(alias="WEBSOCKET_URL")
    region: str = Field(alias="WEBSOCKET_REGION")
    key_id: Optional[str] = Field(alias="WEBSOCKET_KEY_ID", default=None)
    key_secret: Optional[str] = Field(alias="WEBSOCKET_KEY_SECRET", default=None)
