from typing import Optional, List

from fastapi import Depends

from database import SessionLocal, get_db
from database.models import NoteModel, UserModel
from persistence.objects import Note, User


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
        note_model = NoteModel(title=note.title, content=note.content, owner=note.owner, last_edition=note.last_edition)
        self.__db.add(note_model)
        self.__db.commit()
        self.__db.refresh(note_model)
        return note_model.id

    def delete(self, note_id: int):
        self.__db.query(NoteModel).filter(NoteModel.id == note_id).delete()
        self.__db.commit()

    def get_all(self, owner: str) -> List[Note]:
        notes = self.__db.query(NoteModel).filter(NoteModel.owner == owner).all()
        if notes is None:
            return []
        return notes

