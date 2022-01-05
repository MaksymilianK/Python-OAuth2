from typing import Optional

from fastapi import Depends

from src.database import SessionLocal, get_db
from src.database.models import SessionModel
from src.persistence.objects import Session, User


class SessionDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def create(self, session: Session):
        self.__db.add(SessionModel(id=session.id, owner_nick=session.owner.nick))
        self.__db.commit()

    def delete(self, session_id: str):
        self.__db.query(SessionModel).filter(SessionModel.id == session_id).delete()
        self.__db.commit()

    def get_user(self, session_id: str) -> Optional[User]:
        session = self.__db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session is None:
            return None

        return User(nick=session.owner_nick)
