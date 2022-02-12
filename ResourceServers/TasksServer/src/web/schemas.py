from pydantic import Field
from pydantic.main import BaseModel


class TaskBase(BaseModel):
    text: str
    day: str
    status: bool


class TaskCreateRequest(TaskBase):
    pass


class TaskCreateResponse(TaskBase):
    id: int


class TaskRequest(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]


class TaskUpdateStatusResponse(BaseModel):
    status: bool


class AuthTokenBase(BaseModel):
    token: str


class AuthTokenInfoResponse(AuthTokenBase):
    owner: str
    client_id: int = Field(alias="clientId")
    scopes: list[str]
