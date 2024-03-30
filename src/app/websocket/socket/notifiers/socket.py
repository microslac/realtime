import json
from functools import cached_property
from typing import List

import boto3
from botocore.exceptions import ClientError

from .base import Notifier, NotifyError

from app.settings import settings


class SocketNotifier(Notifier):
    @cached_property
    def client(self):
        return boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=settings.websocket.url,
            region_name=settings.websocket.region,
            aws_access_key_id=settings.websocket.key_id,
            aws_secret_access_key=settings.websocket.key_secret,
        )

    def is_enabled(self) -> bool:
        return bool(settings.websocket.url)

    async def notify(
        self, connection_id: str, payload: dict, processed: bytes = None, raise_: bool = False, **kwargs
    ) -> str | None:
        if self.is_enabled():
            try:
                bytes_data = processed or json.dumps(payload).encode("utf-8")
                self.client.post_to_connection(ConnectionId=connection_id, Data=bytes_data)
            except ClientError:
                if raise_:
                    raise NotifyError(connection_id=connection_id)
                return connection_id

    async def notify_many(self, connection_ids: List[str], payload: dict, **kwargs) -> list:
        if not connection_ids:
            return []

        invalid_ids = []
        bytes_data = json.dumps(payload).encode("utf-8")
        for connection_id in connection_ids:
            try:
                await self.notify(connection_id, {}, processed=bytes_data)
            except NotifyError:
                invalid_ids.append(connection_id)
        return invalid_ids
