import logging
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Cookie
from starlette import status
from starlette.responses import Response

from exceptions import NickExistsException, EmailExistsException, EmailNotExistException, WrongPasswordException, \
    UserNotAuthenticatedException, ClientNameExistsException, ClientRedirectURLExistsException, ClientNotFoundException, \
    AuthCodeNotFoundException
from web.schemas import UserCreateRequest, UserSignInRequest, UserResponse, ClientResponse, ClientCreateRequest, \
    AuthCodeRequest, AuthCodeResponse, TokenRequest, TokenResponse, TokenRevocationRequest, TokenIntrospectionRequest, \
    TokenInfoResponse
from services.auth_service import AuthService
from services.client_service import ClientService
from services.user_service import UserService
from config import WebConfig


app = FastAPI()


@app.post(f"{WebConfig.ROUTE_PREFIX}/users", response_model=UserResponse)
def sign_up(response: Response, form: UserCreateRequest, service: UserService = Depends()):

    try:
        user, session_id = service.create(form)
        response.set_cookie(key="SID", value=session_id, max_age=86400)
        return user
    except NickExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    except EmailExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)


@app.post(f"{WebConfig.ROUTE_PREFIX}/current-user", response_model=UserResponse)
def sign_in(response: Response, form: UserSignInRequest, service: UserService = Depends()):
    try:
        user, session_id = service.sign_in(form)
        response.set_cookie(key="SID", value=session_id, max_age=86400)
        return user
    except EmailNotExistException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except WrongPasswordException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.delete(f"{WebConfig.ROUTE_PREFIX}/current-user", status_code=status.HTTP_204_NO_CONTENT)
def sign_out(response: Response, sid: Optional[str] = Cookie(None), service: UserService = Depends()):
    service.sign_out(sid)
    response.set_cookie(key="SID", max_age=0)


@app.get(f"{WebConfig.ROUTE_PREFIX}/current-user", response_model=UserResponse)
def get_current(SID: Optional[str] = Cookie(None), service: UserService = Depends()):
    try:
        return service.get_user(SID)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.get(WebConfig.ROUTE_PREFIX + "/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, service: ClientService = Depends()):
    client = service.get_one(client_id)
    print(client.redirect_url)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=0)

    return ClientResponse(name=client.name, description=client.description, id=client.id, redirectUrl=client.redirect_url)


@app.post(f"{WebConfig.ROUTE_PREFIX}/clients", response_model=ClientResponse)
def create_client(clientRequest: ClientCreateRequest, SID: Optional[str] = Cookie(None),
                  service: ClientService = Depends()):
    try:
        client = service.create(clientRequest, SID)
        return ClientResponse(name=client.name, description=client.description, id=client.id, redirectUrl=client.redirect_url)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNameExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    except ClientRedirectURLExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)


@app.post(f"{WebConfig.ROUTE_PREFIX}/authorization")
async def authorize(auth_request: AuthCodeRequest, SID: Optional[str] = Cookie(None), service: AuthService = Depends()):
    try:
        auth_code_info = await service.authorize(SID, auth_request)
        return AuthCodeResponse(code=auth_code_info.code, redirectUrl=auth_code_info.client.redirect_url)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@app.post(f"{WebConfig.ROUTE_PREFIX}/auth-token")
def get_auth_token(token_request: TokenRequest, service: AuthService = Depends()):
    try:
        token = service.generate_token(token_request.code)
        return TokenResponse(token=token.token, owner=token.owner.nick)
    except AuthCodeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.post(f"{WebConfig.ROUTE_PREFIX}/token-revocation", status_code=204)
def revoke_token(token_request: TokenRevocationRequest, service: AuthService = Depends()):
    service.revoke_token(token_request.token)


@app.post(f"{WebConfig.ROUTE_PREFIX}/token-info", response_model=TokenInfoResponse)
def introspect_token(token_request: TokenIntrospectionRequest, service: AuthService = Depends()):
    try:
        token, active = service.introspect_token(token_request.token)

        logging.info(f'Introspection request for token {token.token_id}')

        return TokenInfoResponse(token_id=token.token_id, owner=token.owner_nick,
                                 clientId=token.client_id, scopes=token.scopes, active=active)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
