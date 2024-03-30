from pydantic import BaseModel


class Message(BaseModel):
    ts: float
    team: str
    user: str
    channel: str
    text: str
    type: str
    subtype: str | None = None
    updated: float | None = None
    metadata: dict | None = None
    client_msg_id: str | None = None
