import secrets

from fastapi import Depends

from src.exceptions import UserNotAuthenticatedException, ClientNotFoundException, AuthCodeNotFoundException
from src.handler.schemas import AuthCodeRequest
from src.persistence.auth_code_dao import AuthCodeDAO
from src.persistence.objects import AuthCodeInfo, AuthToken
from src.persistence.token_dao import TokenDAO
from src.services.client_service import ClientService
from src.services.session_service import SessionService


class AuthService:
    AUTH_CODE_LEN = 16
    TOKEN_LEN = 32

    def __init__(self, session_service: SessionService = Depends(), client_service: ClientService = Depends(),
                 code_dao: AuthCodeDAO = Depends(), token_dao: TokenDAO = Depends()):
        self.__session_service = session_service
        self.__client_service = client_service
        self.__code_dao = code_dao
        self.__token_dao = token_dao

    def authorize(self, session_id: str, auth_request: AuthCodeRequest) -> AuthCodeInfo:
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        client = self.__client_service.get_one(auth_request.client_id)
        if client is None:
            raise ClientNotFoundException()

        code = secrets.token_urlsafe(self.AUTH_CODE_LEN)

        auth_code_info = AuthCodeInfo(code, client, auth_request.scope, user)
        self.__code_dao.store(auth_code_info)
        return auth_code_info

    def generate_token(self, code: str) -> AuthToken:
        auth_code_info = self.__code_dao.get(code)
        if auth_code_info is None:
            raise AuthCodeNotFoundException()

        token_id = secrets.token_urlsafe(self.TOKEN_LEN)

        token = AuthToken(token_id, auth_code_info.owner, auth_code_info.client, auth_code_info.scope)
        self.__token_dao.create(token)
        return token

    def revoke_token(self, token: str):
        self.__token_dao.delete(token)
