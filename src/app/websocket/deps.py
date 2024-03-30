from fastapi import Header


def get_connection_id(connection_id: str = Header(alias="Connectionid")) -> str:
    return connection_id
