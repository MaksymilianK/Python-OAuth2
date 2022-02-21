import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends

from persistence.objects import User, Session
from persistence.session_dao import SessionDAO


class SessionService:
    SESSION_ID_LEN = 32

    def __init__(self, dao: SessionDAO = Depends()):
        self.__dao = dao

    def create(self, owner: User) -> str:
        session_id = secrets.token_urlsafe(self.SESSION_ID_LEN)
        self.__dao.create(Session(session_id, owner.nick, datetime.now() + timedelta(days=1)))
        return session_id

    def delete(self, session_id: str):
        self.__dao.delete(session_id)

    def get_user(self, session_id: str) -> Optional[User]:
        return self.__dao.get_user_for_active(session_id, datetime.now())
