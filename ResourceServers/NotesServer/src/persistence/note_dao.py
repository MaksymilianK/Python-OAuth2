from typing import Optional, List

from fastapi import Depends

from database import SessionLocal, get_db
from database.models import NoteModel
from persistence.objects import Note


class NoteDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

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
        return [Note(n.id, n.title, n.content, n.owner, n.last_edition) for n in notes]

