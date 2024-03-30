import pytest

from app.websocket.schemas import Message


@pytest.fixture
def message():
    msg = Message(
        team="T0123456789",
        user="U0123456789",
        channel="C0123456789",
        text="message",
        type="message",
        ts=1710853582.867723,
    )

    return msg
