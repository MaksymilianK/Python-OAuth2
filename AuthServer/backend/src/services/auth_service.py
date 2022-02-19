import asyncio
import secrets

from fastapi import Depends

from exceptions import UserNotAuthenticatedException, ClientNotFoundException, AuthCodeNotFoundException
from web.schemas import AuthCodeRequest
from persistence.auth_code_dao import AuthCodeDAO
from persistence.objects import AuthCodeInfo, AuthToken
from persistence.token_dao import TokenDAO
from services.client_service import ClientService
from services.session_service import SessionService

from config import OAuth2Config

from datetime import datetime, timedelta

import logging


class AuthService:
    AUTH_CODE_LEN = 16
    TOKEN_LEN = 32

    def __init__(self, session_service: SessionService = Depends(), client_service: ClientService = Depends(),
                 code_dao: AuthCodeDAO = Depends(), token_dao: TokenDAO = Depends()):
        self.__session_service = session_service
        self.__client_service = client_service
        self.__code_dao = code_dao
        self.__token_dao = token_dao

    async def authorize(self, session_id: str, auth_request: AuthCodeRequest) -> AuthCodeInfo:
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        client = self.__client_service.get_one(auth_request.client_id)
        if client is None:
            raise ClientNotFoundException()

        code = secrets.token_urlsafe(self.AUTH_CODE_LEN)

        auth_code_info = AuthCodeInfo(code, client.id, auth_request.scope, user.nick)
        self.__code_dao.store(auth_code_info)

        logging.info(f'Store authorization code {code}')

        asyncio.get_running_loop().call_later(OAuth2Config.AUTH_CODE_LIFETIME, lambda: self._remove_code(code))

        return auth_code_info

    def generate_token(self, code: str) -> AuthToken:
        auth_code_info = self.__code_dao.get(code)
        if auth_code_info is None:
            raise AuthCodeNotFoundException()

        token_id = secrets.token_urlsafe(self.TOKEN_LEN)

        token = AuthToken(token_id, auth_code_info.owner_nick, auth_code_info.client_id, auth_code_info.scope,
                          datetime.now() + timedelta(days=7))
        self.__token_dao.create(token)
        self.__code_dao.delete(code)

        logging.info(f'Store authorization token {token_id} for client {auth_code_info.client_id} & owner {auth_code_info.owner_nick}')

        return token

    def revoke_token(self, token: str):
        self.__token_dao.update_date(token, datetime.now())

        logging.info(f'Revoke token {token}')

    def introspect_token(self, token: str):
        token = self.__token_dao.get(token)
        if token is None:
            raise UserNotAuthenticatedException

        active = token.date > datetime.now()

        return token, active

    def _remove_code(self, code: str):
        if self.__code_dao.delete(code):
            logging.info(f'Code {code} expired')
