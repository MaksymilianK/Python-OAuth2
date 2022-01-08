from datetime import time, datetime

from fastapi import Depends


from src.handler.schemas import NoteCreateRequest
from src.persistence.note_dao import NoteDAO
from src.persistence.objects import Note
from src.services.introspection_fasade import IntrospectionFacade


class NoteService:
    def __init__(self, introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                 dao: NoteDAO = Depends(NoteDAO)):
        self.__introspection_facade = introspection_facade
        self.__dao = dao

    def create(self, note_request: NoteCreateRequest, owner: str) -> Note:
        note = Note(
            title=note_request.title,
            content=note_request.content,
            owner=owner,
            last_edition=datetime.now()
        )

        note.id = self.__dao.create(note)
        return note
