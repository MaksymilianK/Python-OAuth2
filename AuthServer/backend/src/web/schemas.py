from pydantic import Field
from pydantic.main import BaseModel


NICK_REGEX = r"^\w{3,16}$"
EMAIL_REGEX = r"^\S+@\S+(\.\S+)+$"


class UserBase(BaseModel):
    nick: str = Field(regex=NICK_REGEX)


class UserCreateRequest(UserBase):
    email: str = Field(regex=EMAIL_REGEX)
    password: str = Field(min_length=7, max_length=100)


class UserResponse(UserBase):
    class Config:
        orm_mode = True


class UserSignInRequest(BaseModel):
    email: str = Field(regex=EMAIL_REGEX)
    password: str = Field(min_length=7, max_length=100)


class ExceptionResponse(BaseModel):
    description: str
    code: int


class ClientBase(BaseModel):
    name: str
    description: str


class ClientCreateRequest(ClientBase):
    redirect_url: str = Field(alias="redirectUrl", min_length=1)


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
    scopes: list[str]
    active: bool


class AuthCodeRequest(BaseModel):
    client_id: int = Field(alias="clientId")
    scope: list[str]


class AuthCodeResponse(BaseModel):
    code: str
    redirect_url: str = Field(alias="redirectUrl")

    class Config:
        orm_mode = True


class SavedScopeUpdateRequest(BaseModel):
    client_id: int = Field(alias="clientId")
    scope: list[str]


class ClientSavedScopeResponse(BaseModel):
    scope: list[str]


class SavedScopeResponse(BaseModel):
    scopes: list[tuple[ClientSavedScopeResponse, ClientResponse]]
