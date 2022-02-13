from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel
from typing import List


class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    content: str = Field(min_length=1, max_length=250)


class NoteCreateRequest(NoteBase):
    pass


class NoteDeleteRequest(BaseModel):
    id: int


class NoteCreateResponse(BaseModel):
    id: int
    last_edition: datetime = Field(alias="lastEdition")


class NoteResponse(NoteBase):
    id: int
    owner: str
    last_edition: datetime = Field(alias="lastEdition")

    class Config:
        orm_mode = True


class NoteListResponse(BaseModel):
    notes: List[NoteResponse]


class AuthTokenBase(BaseModel):
    token: str


class AuthTokenInfoResponse(AuthTokenBase):
    owner: str
    client_id: int = Field(alias="clientId")
    scopes: List[str]
