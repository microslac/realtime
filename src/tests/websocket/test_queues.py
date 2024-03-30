import pytest
from faststream.rabbit import TestRabbitBroker

from app.websocket.queues import exchange, message_handler, router


@pytest.mark.asyncio()
async def test_handle_message(message):
    async with TestRabbitBroker(router.broker) as broker:
        data = message.model_dump()
        await broker.publish(data, routing_key="message.created", exchange=exchange)
        message_handler.mock.assert_called_once_with(data)
