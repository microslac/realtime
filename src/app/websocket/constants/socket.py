from enum import StrEnum


class SocketType(StrEnum):
    PING = "ping"
    PONG = "pong"
    HELLO = "hello"
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    MESSAGE = "message"
    USER_TYPING = "user_typing"
    PRESENCE_SUB = "presence_sub"
    PRESENCE_CHANGED = "presence_changed"
    USER_PROFILE_CHANGED = "user_profile_changed"
    CHANNEL_MEMBER_JOINED = "channel_member_joined"


class SocketSubtype(StrEnum):
    MESSAGE_REPLIED = "message_replied"
    MESSAGE_CHANGED = "message_changed"
    MESSAGE_DELETED = "message_deleted"
    CHANNEL_JOINED = "channel_joined"
