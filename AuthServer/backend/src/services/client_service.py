from fastapi import Depends

from src.handler.schemas import ClientCreateRequest
from src.persistence.client_dao import ClientDAO
from src.persistence.objects import User, Client
from src.exceptions import  ClientNameExistsException, ClientRedirectURLExistsException


class UserService:
    def __init__(self, dao: ClientDAO = Depends(ClientDAO)):
        self.__dao = dao

    def create(self, client_request: ClientCreateRequest, owner: User) -> Client:
        if self.__dao.exists_by_name(client_request.name):
            raise ClientNameExistsException()
        elif self.__dao.exists_by_redirect_url(client_request.redirect_url):
            raise ClientRedirectURLExistsException()

        client = Client(
            name=client_request.name,
            description=client_request.description,
            redirect_url=client_request.redirect_url,
            owner=owner
        )

        client.id = self.__dao.create(client)
        return client
