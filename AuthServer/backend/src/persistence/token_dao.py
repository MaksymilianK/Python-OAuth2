from datetime import datetime

from pydantic.fields import Optional
from sqlalchemy import and_

from fastapi import Depends

from database import SessionLocal, get_db
from database.models import TokenModel
from exceptions import TokenNotFoundException
from persistence.objects import AuthToken, User, Client, SavedScope


class TokenDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def create(self, token: AuthToken):
        self.__db.add(TokenModel(
            token_id=token.token,
            owner_nick=token.owner_nick,
            client_id=token.client_id,
            scopes=token.scope,
            date=token.date
        ))
        self.__db.commit()

    def update_date(self, token: str, date: datetime):
        token = self.__db.query(TokenModel).filter(TokenModel.token_id == token).first()

        if token is None:
            raise TokenNotFoundException()

        token.date = date
        self.__db.commit()

    def get(self, token: str) -> Optional[AuthToken]:
        model = self.__db.query(TokenModel).filter(TokenModel.token_id == token).first()
        if model is None:
            return None

        return AuthToken(token=token, owner_nick=model.owner_nick, client_id=model.client_id, date=model.date)

    def get_all_before(self, date: datetime, nick: str) -> list[AuthToken]:
        auth_tokens = self.__db.query(TokenModel).filter(and_(TokenModel.date > date, TokenModel.owner_nick == nick)).all()

        return [AuthToken(token=t.token_id, client_id=t.client_id, date=t.date) for t in auth_tokens]

    def update_scopes(self, saved_scope: SavedScope):
        tokens = self.__db.query(TokenModel)\
            .filter(and_(
                TokenModel.owner_nick == saved_scope.user_nick,
                TokenModel.client_id == saved_scope.client_id
            ))\
            .all()

        for token in tokens:
            token.scope = saved_scope.scope

        self.__db.commit()
