from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel
from typing import List


class PublicationBase(BaseModel):
    content: str = Field(min_length=1, max_length=250)


class PublicationCreateRequest(PublicationBase):
    pass


class PublicationDeleteRequest(BaseModel):
    id: int


class PublicationEditRequest(BaseModel):
    id: int
    content: str = Field(min_length=1, max_length=250)


class PublicationCreateResponse(BaseModel):
    id: int
    last_edition: str = Field(alias="lastEdition")


class PublicationEditResponse(BaseModel):
    last_edition: str = Field(alias="lastEdition")


class PublicationResponse(PublicationBase):
    id: int
    owner: str
    last_edition: str = Field(alias="lastEdition")

    class Config:
        orm_mode = True


class PublicationListResponse(BaseModel):
    publications: List[PublicationResponse]


class AuthTokenBase(BaseModel):
    token: str


class AuthTokenInfoResponse(AuthTokenBase):
    owner: str
    client_id: int = Field(alias="clientId")
    scopes: List[str]
