from src.database import SessionLocal
from src.database.models import ClientModel
from src.persistence.objects import Client


class ClientDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def exists_by_name(self, name: str) -> bool:
        return self.__db.query(ClientModel).filter(ClientModel.name == name).first() is not None

    def exists_by_redirect_url(self, redirect_url: str) -> bool:
        return self.__db.query(ClientModel).filter(ClientModel.redirect_url == redirect_url).first() is not None

    def create(self, client: Client) -> int:
        client_model = ClientModel(
            name=client.name,
            description=client.description,
            redirect_url=client.redirect_url,
            owner_nick=client.owner.nick
        )
        self.__db.add(client_model)

        self.__db.commit()
        self.__db.refresh(client_model)

        return client_model.id
