from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Cookie
from starlette import status
from starlette.responses import Response

from src.database import engine, Base
from src.exceptions import NickExistsException, EmailExistsException, EmailNotExistException, WrongPasswordException, \
    UserNotAuthenticatedException, ClientNameExistsException, ClientRedirectURLExistsException
from src.handler.schemas import UserCreateRequest, UserSignInRequest, UserResponse, ClientResponse, ClientCreateRequest
from src.services.client_service import ClientService
from src.services.user_service import UserService

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/auth/api/users", response_model=UserResponse)
def sign_up(response: Response, user: UserCreateRequest, service: UserService = Depends(UserService)):
    try:
        user, session_id = service.create(user)
        response.set_cookie(key="SID", value=session_id, expires=2147483647)
        return user
    except NickExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    except EmailExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)


@app.post("/auth/api/current-user", response_model=UserResponse)
def sign_in(response: Response, form: UserSignInRequest, service: UserService = Depends(UserService)):
    try:
        user, session_id = service.sign_in(form)
        response.set_cookie(key="SID", value=session_id, expires=2147483647)
        return user
    except EmailNotExistException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except WrongPasswordException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.delete("/auth/api/current-user", status_code=status.HTTP_204_NO_CONTENT)
def sign_out(response: Response, sid: Optional[str] = Cookie(None), service: UserService = Depends(UserService)):
    service.sign_out(sid)
    response.set_cookie(key="SID", expires=0)


@app.get("/auth/api/current-user", response_model=UserResponse)
def get_current(SID: Optional[str] = Cookie(None), service: UserService = Depends(UserService)):
    try:
        return service.get_user(SID)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.post("/auth/api/clients", response_model=ClientResponse)
def create_client(client: ClientCreateRequest, SID: Optional[str] = Cookie(None),
                  service: ClientService = Depends(ClientService)):
    try:
        return service.create(client, SID)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNameExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    except ClientRedirectURLExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
