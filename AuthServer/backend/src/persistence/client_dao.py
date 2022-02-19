from typing import Optional

from fastapi import Depends

from database import SessionLocal, get_db
from database.models import ClientModel
from .objects import Client


class ClientDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def exists(self, id: int) -> bool:
        return self.__db.query(ClientModel).filter(ClientModel.id == id).first() is not None

    def exists_by_name(self, name: str) -> bool:
        return self.__db.query(ClientModel).filter(ClientModel.name == name).first() is not None

    def exists_by_redirect_url(self, redirect_url: str) -> bool:
        return self.__db.query(ClientModel).filter(ClientModel.redirect_url == redirect_url).first() is not None

    def get_one(self, client_id: int) -> Optional[Client]:
        client_model = self.__db.query(ClientModel).filter(ClientModel.id == client_id).first()
        if client_model is None:
            return None

        return Client(client_model.id, client_model.name, client_model.description, client_model.redirect_url)

    def create(self, client: Client) -> int:
        client_model = ClientModel(
            name=client.name,
            description=client.description,
            redirect_url=client.redirect_url,
            owner_nick=client.owner_nick
        )
        self.__db.add(client_model)

        self.__db.commit()
        self.__db.refresh(client_model)

        return client_model.id
