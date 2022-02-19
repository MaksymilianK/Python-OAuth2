from typing import Optional

from fastapi import Depends
from sqlalchemy import and_

from database import SessionLocal, get_db
from database.models import SavedScopeModel
from persistence.objects import SavedScope


class SavedScopeDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def get_for_user(self, user_nick: str) -> list[SavedScope]:
        models = self.__db.query(SavedScopeModel).filter(SavedScopeModel.user_nick == user_nick).all()
        return [SavedScope(m.user_nick, m.client_id, m.scopes) for m in models]

    def get_for_user_and_client(self, user_nick: str, client_id: int) -> Optional[SavedScope]:
        model = self.__db.query(SavedScopeModel) \
            .filter(and_(
                    SavedScopeModel.user_nick == user_nick,
                    SavedScopeModel.client_id == client_id
                    ))\
            .first()

        if model is None:
            return None

        return SavedScope(user_nick, client_id, model.scopes)

    def create(self, saved_scope: SavedScope):
        self.__db.add(SavedScopeModel(
            user_nick=saved_scope.user_nick,
            client_id=saved_scope.client_id,
            scopes=saved_scope.scope,
        ))
        self.__db.commit()

    def update(self, saved_scope: SavedScope):
        model = self.__db.query(SavedScopeModel)\
            .filter(and_(
                    SavedScopeModel.user_nick == saved_scope.user_nick,
                    SavedScopeModel.client_id == saved_scope.client_id
                    ))\
            .first()

        model.scopes = saved_scope.scope
        self.__db.commit()
