import logging
import secrets
from datetime import datetime, timedelta

from fastapi import Depends

from exceptions import AuthCodeNotFoundException, UserNotAuthenticatedException
from persistence.auth_code_dao import AuthCodeDAO
from persistence.objects import AuthToken, SavedScope
from persistence.token_dao import TokenDAO


class TokenService:
    TOKEN_LEN = 32

    def __init__(self, code_dao: AuthCodeDAO = Depends(), token_dao: TokenDAO = Depends()):
        self.__code_dao = code_dao
        self.__token_dao = token_dao

    def generate_token(self, code: str) -> AuthToken:
        auth_code_info = self.__code_dao.get(code)
        if auth_code_info is None:
            raise AuthCodeNotFoundException()

        token_id = secrets.token_urlsafe(self.TOKEN_LEN)

        token = AuthToken(token_id, auth_code_info.owner_nick, auth_code_info.client_id, auth_code_info.scope,
                          datetime.now() + timedelta(days=7))
        self.__token_dao.create(token)
        self.__code_dao.delete(code)

        logging.info(f"Store authorization token '{token_id}' for client with id {auth_code_info.client_id} & owner '{auth_code_info.owner_nick}'")

        return token

    def revoke_token(self, token: str):
        self.__token_dao.update_date(token, datetime.now())

        logging.info(f"Revoke token '{token}'")

    def introspect_token(self, token: str):
        token = self.__token_dao.get(token)
        if token is None:
            raise UserNotAuthenticatedException

        active = token.date > datetime.now()

        return token, active

    def update_scope(self, saved_scope: SavedScope):
        self.__token_dao.update_scopes(saved_scope, datetime.now())

        logging.info(f"Update scope of active tokens for user '{saved_scope.user_nick}'")
