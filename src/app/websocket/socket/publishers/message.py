import asyncio

from .base import Publisher

from app.websocket.constants import SocketType
from app.websocket.socket.stores import keys


class MessagePublisher(Publisher):
    def clean(self):
        cid = self.ctx.payload.get("channel")
        uids = self.ctx.payload.get("members") or []
        msg = self.ctx.payload.get("message") or {}
        is_valid = all([cid, uids, msg])
        msg.update(type=SocketType.MESSAGE)

        return is_valid, cid, uids, msg

    async def publish(self) -> dict:
        is_valid, channel_id, user_ids, message = self.clean()

        if is_valid:
            fetch_tasks = [self.store.all(keys.user_conns.format(user_id)) for user_id in user_ids]
            connection_ids_results = await asyncio.gather(*fetch_tasks)

            async def handle_user(user_index):
                user_id = user_ids[user_index]
                connection_ids = connection_ids_results[user_index]
                invalid_connection_ids = await self.notifier.notify_many(list(connection_ids), payload=message)
                if invalid_connection_ids:
                    await self.store.remove(key=keys.user_conns.format(user_id), values=invalid_connection_ids)

            await asyncio.gather(*(handle_user(index) for index in range(len(user_ids))))

        return {}
