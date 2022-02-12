from typing import List

from pydantic import Field
from pydantic.main import BaseModel


class UserBase(BaseModel):
    nick: str


class UserCreateRequest(UserBase):
    email: str
    password: str


class UserResponse(UserBase):
    class Config:
        orm_mode = True


class UserSignInRequest(BaseModel):
    email: str
    password: str


class ExceptionResponse(BaseModel):
    description: str
    code: int


class ClientBase(BaseModel):
    name: str
    description: str


class ClientCreateRequest(ClientBase):
    redirect_url: str = Field(alias="redirectUrl")


class ClientIdResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ClientResponse(ClientBase):
    id: int
    redirect_url: str = Field(alias="redirectUrl")

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    id: str


class SessionCreate(SessionBase):
    owner: UserBase


class TokenBase(BaseModel):
    token_id: str


class TokenRequest(BaseModel):
    code: str


class TokenRevocationRequest(BaseModel):
    token: str


class TokenIntrospectionRequest(BaseModel):
    token: str


class TokenResponse(BaseModel):
    token: str = Field(alias="token")
    owner: str

    class Config:
        orm_mode = True


class TokenInfoResponse(TokenBase):
    owner: str
    client_id: int = Field(alias="clientId")
    scopes: List[str]


class AuthCodeRequest(BaseModel):
    client_id: int = Field(alias="clientId")
    scope: List[str]


class AuthCodeResponse(BaseModel):
    code: str
    redirect_url: str = Field(alias="redirectUrl")

    class Config:
        orm_mode = True