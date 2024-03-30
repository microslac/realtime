from .base import EnvSettings, Field


class RabbitSettings(EnvSettings):
    protocol: str = Field(alias="QUEUE_PROTOCOL", default="amqp")
    host: str = Field(alias="QUEUE_HOST", default="localhost")
    port: int = Field(alias="QUEUE_PORT", default=5672)
    username: str = Field(alias="QUEUE_USERNAME")
    password: str = Field(alias="QUEUE_PASSWORD")

    @property
    def url(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}/"
