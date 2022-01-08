from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Cookie
from starlette import status
from starlette.responses import Response

from src.database import engine, Base
from src.exceptions import NickExistsException, EmailExistsException, EmailNotExistException, WrongPasswordException, \
    UserNotAuthenticatedException, ClientNameExistsException, ClientRedirectURLExistsException, ClientNotFoundException, \
    AuthCodeNotFoundException
from src.handler.schemas import UserCreateRequest, UserSignInRequest, UserResponse, ClientResponse, ClientCreateRequest, \
    AuthCodeRequest, AuthCodeResponse, TokenRequest, TokenResponse, TokenRevocationRequest
from src.services.auth_service import AuthService
from src.services.client_service import ClientService
from src.services.user_service import UserService

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/my-auth/api/users", response_model=UserResponse)
def sign_up(response: Response, user: UserCreateRequest, service: UserService = Depends(UserService)):
    try:
        user, session_id = service.create(user)
        response.set_cookie(key="SID", value=session_id, expires=2147483647)
        return user
    except NickExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    except EmailExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)


@app.post("/my-auth/api/current-user", response_model=UserResponse)
def sign_in(response: Response, form: UserSignInRequest, service: UserService = Depends(UserService)):
    try:
        user, session_id = service.sign_in(form)
        response.set_cookie(key="SID", value=session_id, expires=2147483647)
        return user
    except EmailNotExistException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except WrongPasswordException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.delete("/my-auth/api/current-user", status_code=status.HTTP_204_NO_CONTENT)
def sign_out(response: Response, sid: Optional[str] = Cookie(None), service: UserService = Depends(UserService)):
    service.sign_out(sid)
    response.set_cookie(key="SID", expires=0)


@app.get("/my-auth/api/current-user", response_model=UserResponse)
def get_current(SID: Optional[str] = Cookie(None), service: UserService = Depends(UserService)):
    try:
        return service.get_user(SID)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.get("/my-auth/api/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, service: ClientService = Depends(ClientService)):
    client = service.get_one(client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=0)

    return client


@app.post("/my-auth/api/clients", response_model=ClientResponse)
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


@app.post("/my-auth/api/authorization")
def authorize(auth_request: AuthCodeRequest, SID: Optional[str] = Cookie(None), service: AuthService = Depends()):
    try:
        auth_code_info = service.authorize(SID, auth_request)
        print("------", auth_code_info.client.redirect_url)
        return AuthCodeResponse(code=auth_code_info.code, redirectUrl=auth_code_info.client.redirect_url)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@app.post("/my-auth/api/auth-token")
def get_auth_token(token_request: TokenRequest, service: AuthService = Depends()):
    try:
        token = service.generate_token(token_request.code)
        return TokenResponse(token=token.token, owner=token.owner.nick)
    except AuthCodeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.post("/my-auth/api/token-revocation", status_code=204)
def revoke_token(token_request: TokenRevocationRequest, service: AuthService = Depends()):
    service.revoke_token(token_request.token)
