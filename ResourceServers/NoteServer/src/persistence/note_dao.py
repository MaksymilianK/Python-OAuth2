from typing import Optional

from fastapi import Depends

from src.database import SessionLocal, get_db
from src.database.models import NoteModel
from src.persistence.objects import Note


class NoteDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def exists_with_nick(self, nick: str) -> bool:
        return self.__db.query(UserModel).filter(UserModel.nick == nick).first() is not None

    def exists_with_email(self, email: str) -> bool:
        return self.__db.query(UserModel).filter(UserModel.email == email).first() is not None

    def get_one_by_email(self, email: str) -> Optional[User]:
        user = self.__db.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            return None

        return User(nick=user.nick, password=user.password_hash)

    def create(self, note: Note) -> int:
        note_model = NoteModel(title=note.title, content=note.content, owner=note.owner)
        self.__db.add(note_model)
        self.__db.commit()

        self.__db.refresh(note_model)
        return note_model.id
