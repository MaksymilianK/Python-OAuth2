import logging
from datetime import datetime
from typing import Optional

from fastapi import Depends

from exceptions import UserNotAuthenticatedException
from persistence.objects import SavedScope, Client
from persistence.saved_scope_dao import SavedScopeDAO
from services.client_service import ClientService
from services.session_service import SessionService
from services.token_service import TokenService


class SavedScopeService:
    def __init__(self, dao: SavedScopeDAO = Depends(), client_service: ClientService = Depends(),
                 session_service: SessionService = Depends(), token_service: TokenService = Depends()):
        self.__dao = dao
        self.__client_service = client_service
        self.__session_service = session_service
        self.__token_service = token_service

    def get_for_user(self, session_id: str) -> list[tuple[SavedScope, Client]]:
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        saved_scopes = self.__dao.get_for_user(user.nick)
        clients = []
        for scope in saved_scopes:
            clients.append(self.__client_service.get_one(scope.client_id))

        return zip(saved_scopes, clients)

    def get_for_user_and_client(self, client_id: int, session_id: str) -> Optional[SavedScope]:
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        return self.__dao.get_for_user_and_client(user.nick, client_id)

    def save(self, client_id: int, scope: list[str], session_id: str):
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        saved_scope = self.get_for_user_and_client(client_id, session_id)

        if saved_scope is None:
            self.__dao.create(SavedScope(user.nick, client_id, scope))
        else:
            self.__dao.update(SavedScope(user.nick, client_id, scope))

        logging.info(f"Saved new scope for client {client_id}, user '{user.nick}'; scopes: {scope}")

    def revoke_scope(self, client_id: int, session_id: str):
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        self.__dao.update(SavedScope(user.nick, client_id, []))
        self.__token_service.update_scope(SavedScope(user.nick, client_id, []))

        logging.info(f"Revoked scope for client {client_id}, user '{user.nick}'")
