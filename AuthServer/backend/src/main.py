from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Cookie
from starlette import status
from starlette.responses import Response

from src.database import engine, Base
from src.exceptions import NickExistsException, EmailExistsException, EmailNotExistException, WrongPasswordException, \
    UserNotAuthenticatedException
from src.handler.schemas import UserCreateRequest, UserSignInRequest, UserResponse
from src.services.user_service import UserService

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/auth/api/users", status_code=204)
def create_user(response: Response, user: UserCreateRequest, service: UserService = Depends(UserService)):
    try:
        session_id = service.create_user(user)
        response.set_cookie(key="SID", value=session_id)
    except NickExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)
    except EmailExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.detail)


@app.post("/auth/api/current-user", status_code=204)
def sign_in(response: Response, form: UserSignInRequest, service: UserService = Depends(UserService)):
    try:
        session_id = service.sign_in(form)
        response.set_cookie(key="SID", value=session_id)
    except EmailNotExistException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except WrongPasswordException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@app.delete("/auth/api/current-user", status_code=status.HTTP_204_NO_CONTENT)
def sign_out(response: Response, sid: Optional[str] = Cookie(None), service: UserService = Depends(UserService)):
    service.sign_out(sid)
    response.set_cookie(key="SID", expires=0)


@app.get("/auth/api/current-user", response_model=UserResponse)
def get_current(sid: Optional[str] = Cookie(None), service: UserService = Depends(UserService)):
    print("lolxd")
    try:
        return service.get_user(sid)
    except UserNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
