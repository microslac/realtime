from micro.services.registry import ConversationsService

from app.websocket.constants import SocketType
from app.websocket.socket import Handler, keys


class UserTypingHandler(Handler):
    async def handle(self) -> dict:
        channel_id = self.ctx.data.get("channel")
        user_id = await self.store.get(keys.conns.format(self.ctx.connection_id))
        if channel_id and user_id:
            member_ids = await self.get_member_ids(channel_id, user_id)
            payload = dict(type=SocketType.USER_TYPING, channel=channel_id, user=user_id)
            for member_id in member_ids:
                connection_ids = await self.store.all(keys.user_conns.format(member_id))
                invalid_connection_ids = await self.notifier.notify_many(connection_ids, payload=payload)
                await self.store.remove_many(keys=keys.user_conns.format(user_id), values=invalid_connection_ids)

        return {}

    async def get_member_ids(self, channel_id: str, exclude_id: str = "") -> list[str]:
        key = keys.channel_members.format(channel_id)
        member_ids = await self.store.all(key)
        if not member_ids:
            member_ids: list[str] = ConversationsService.post(
                "/internal/members", data=dict(channel=channel_id, all_members=True), internal=True, key="members"
            )
            await self.store.add_all(key, member_ids)
        member_ids = [i for i in member_ids if i != exclude_id]
        return member_ids
