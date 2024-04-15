from app.websocket.services import presence
from app.websocket.socket import Handler, keys


class DisconnectHandler(Handler):
    async def handle(self) -> dict:
        connection_id = self.ctx.connection_id
        user_id = await self.store.get(keys.conns.format(connection_id))
        if user_id:
            await presence.heartbeat(user_id, active=False)
            await self.clear_subscriptions(user_id)
            await self.store.delete(keys.conns.format(connection_id))
            await self.store.remove(keys.user_conns.format(user_id), [connection_id])
            # TODO: resend presence_sub again before keys.user_subs expire (6 hours)
        return {}

    async def clear_subscriptions(self, user_id: str):
        # Get all subscribers' connection_ids
        subscriber_connection_ids = await self.store.all(keys.user_subs.format(user_id))
        for connection_id in subscriber_connection_ids:
            # Use connection_id to query user_id
            subscriber_id = await self.store.get(keys.conns.format(connection_id))
            if subscriber_id:
                # Remove user_id under this subscriber's subs, since the current user is logged out
                await self.store.remove(key=keys.user_subs.format(subscriber_id), values=[self.ctx.connection_id])
