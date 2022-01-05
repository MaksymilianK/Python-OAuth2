from typing import Optional

from fastapi import Depends

from src.database import SessionLocal, get_db
from src.database.models import UserModel
from src.persistence.objects import User


class UserDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def exists_with_nick(self, nick: str) -> bool:
        return self.__db.query(UserModel).filter(UserModel.nick == nick).exists()

    def exists_with_email(self, email: str) -> bool:
        return self.__db.query(UserModel).filter(UserModel.email == email).exists()

    def get_one_by_email(self, email: str) -> Optional[User]:
        user = self.__db.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            return None

        return User(nick=user.nick, password=user.password_hash)

    def create(self, user: User):
        self.__db.add(UserModel(nick=user.nick, email=user.email, password_hash=user.password))
        self.__db.commit()
