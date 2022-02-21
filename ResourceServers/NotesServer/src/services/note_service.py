import logging
from datetime import datetime
from typing import List

from fastapi import Depends


from web.schemas import NoteCreateRequest, NoteListResponse
from persistence.note_dao import NoteDAO
from persistence.objects import Note
from services.introspection_fasade import IntrospectionFacade


class NoteService:
    def __init__(self, introspection_facade: IntrospectionFacade = Depends(), dao: NoteDAO = Depends()):
        self.__introspection_facade = introspection_facade
        self.__dao = dao

    def create(self, note_request: NoteCreateRequest, owner: str) -> Note:
        note = Note(
            title=note_request.title,
            content=note_request.content,
            owner=owner,
            last_edition=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        note.id = self.__dao.create(note)

        logging.info(f"Create note with id {note.id}")

        return note

    def delete(self, note_id: int):
        self.__dao.delete(note_id)

        logging.info(f"Delete note with id {note_id}")

    def get_notes(self, owner: str) -> List[Note]:
        return self.__dao.get_all(owner)
