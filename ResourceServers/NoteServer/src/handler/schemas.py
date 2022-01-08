from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreateRequest(NoteBase):
    pass


class NoteIdResponse(BaseModel):
    id: int


class NoteResponse(NoteBase):
    id: int
    owner: str
    last_edition: datetime = Field(alias="lastEdition")

    class Config:
        orm_mode = True


class NoteListResponse(BaseModel):
    notes: list[NoteResponse]


class AuthTokenBase(BaseModel):
    token: str


class AuthTokenInfoResponse(AuthTokenBase):
    owner: str
    client_id: int = Field(alias="clientId")
    scopes: list[str]
