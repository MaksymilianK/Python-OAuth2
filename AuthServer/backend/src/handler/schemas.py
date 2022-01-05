from typing import Optional

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


class ClientResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    id: str


class SessionCreate(SessionBase):
    owner: UserBase
