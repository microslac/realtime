from pydantic import BaseModel, Field


class Token(BaseModel):
    auth: str = Field(alias="aid")
    team: str = Field(alias="tid")
    user: str = Field(alias="uid")
