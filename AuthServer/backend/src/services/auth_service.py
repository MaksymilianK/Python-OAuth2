import asyncio
import secrets

from fastapi import Depends

from exceptions import UserNotAuthenticatedException, ClientNotFoundException
from services.saved_scope_service import SavedScopeService
from web.schemas import AuthCodeRequest
from persistence.auth_code_dao import AuthCodeDAO
from persistence.objects import AuthCodeInfo
from services.client_service import ClientService
from services.session_service import SessionService

from config import OAuth2Config

import logging


class AuthService:
    AUTH_CODE_LEN = 16

    def __init__(self, session_service: SessionService = Depends(), client_service: ClientService = Depends(),
                 code_dao: AuthCodeDAO = Depends(), saved_scope_service: SavedScopeService = Depends()):
        self.__session_service = session_service
        self.__client_service = client_service
        self.__code_dao = code_dao
        self.__saved_scope_service = saved_scope_service

    async def authorize(self, session_id: str, auth_request: AuthCodeRequest) -> tuple[AuthCodeInfo, str]:
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        client = self.__client_service.get_one(auth_request.client_id)
        if client is None:
            raise ClientNotFoundException()

        code = secrets.token_urlsafe(self.AUTH_CODE_LEN)

        auth_code_info = AuthCodeInfo(code, client.id, auth_request.scope, user.nick)
        self.__code_dao.store(auth_code_info)

        logging.info(f"Store authorization code '{code}'")

        self.__saved_scope_service.save(client.id, auth_request.scope, session_id)

        asyncio.get_running_loop().call_later(OAuth2Config.AUTH_CODE_LIFETIME, lambda: self._remove_code(code))

        return auth_code_info, client.redirect_url

    def _remove_code(self, code: str):
        if self.__code_dao.delete(code):
            logging.info(f"Code '{code}' expired")
