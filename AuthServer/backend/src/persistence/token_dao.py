from fastapi import Depends

from database import SessionLocal, get_db
from database.models import TokenModel, SessionModel
from persistence.objects import AuthToken, User


class TokenDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def create(self, token: AuthToken):
        self.__db.add(TokenModel(
            token_id=token.token,
            owner_nick=token.owner.nick,
            client_id=token.client.id,
            scopes=token.scope
        ))
        self.__db.commit()

    def delete(self, token: str):
        self.__db.query(TokenModel).filter(TokenModel.token_id == token).delete()
        self.__db.commit()

    def get(self, token: str):
        return self.__db.query(TokenModel).filter(TokenModel.token_id == token).first()
