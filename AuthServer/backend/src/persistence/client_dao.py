from src.database import SessionLocal
from src.database.models import ClientModel
from src.persistence.objects import Client


class ClientDAO:
    def create(self, db: SessionLocal, client: Client) -> int:
        client_model = ClientModel(
            name=client.name,
            description=client.description,
            redirect_url=client.redirect_url,
            owner_nick=client.owner.nick
        )
        db.add(client_model)
        db.commit()

        db.refresh(client_model)
        return client_model.id
