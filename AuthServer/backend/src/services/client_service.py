import logging
from typing import Optional

from fastapi import Depends

from web.schemas import ClientCreateRequest
from persistence.client_dao import ClientDAO
from persistence.objects import Client
from exceptions import ClientNameExistsException, ClientRedirectURLExistsException, UserNotAuthenticatedException
from services.session_service import SessionService


class ClientService:
    def __init__(self, session_service: SessionService = Depends(), dao: ClientDAO = Depends()):
        self.__session_service = session_service
        self.__dao = dao

    def create(self, client_request: ClientCreateRequest, session_id: Optional[str]) -> Client:
        current = self.__session_service.get_user(session_id)
        if current is None:
            raise UserNotAuthenticatedException()

        if self.__dao.exists_by_name(client_request.name):
            raise ClientNameExistsException()
        elif self.__dao.exists_by_redirect_url(client_request.redirect_url):
            raise ClientRedirectURLExistsException()

        client = Client(
            name=client_request.name,
            description=client_request.description,
            redirect_url=client_request.redirect_url,
            owner_nick=current.nick
        )

        client.id = self.__dao.create(client)

        logging.info(f"Create client '{client.name}' with id {client.id}")

        return client

    def exists(self, client_id: int) -> bool:
        return self.__dao.exists(client_id)

    def get_one(self, client_id: int) -> Optional[Client]:
        return self.__dao.get_one(client_id)
