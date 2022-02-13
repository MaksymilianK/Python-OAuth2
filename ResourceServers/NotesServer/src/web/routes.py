from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from database import engine, Base
from exceptions import ClientNotAuthenticatedException, ClientNotAuthorizedException
from .schemas import NoteCreateRequest, NoteResponse, NoteListResponse, NoteCreateResponse, NoteDeleteRequest
from services.introspection_fasade import IntrospectionFacade
from services.note_service import NoteService

from config import OAuth2Config, WebConfig


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post(f"{WebConfig.ROUTE_PREFIX}/add-note", status_code=HTTP_201_CREATED, response_model=NoteCreateResponse)
async def create_note(request: Request, note: NoteCreateRequest, introspection_facade: IntrospectionFacade = Depends(),
                      service: NoteService = Depends()):
    try:
        owner = await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_CREATE_NOTES])
        note_create_response = service.create(note, owner)
        return NoteCreateResponse(id=note_create_response.id, lastEdition=note_create_response.last_edition)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.delete(f"{WebConfig.ROUTE_PREFIX}/delete-note", status_code=HTTP_204_NO_CONTENT)
async def delete_note(request: Request, note: NoteDeleteRequest, introspection_facade: IntrospectionFacade = Depends(),
                      service: NoteService = Depends()):
    try:
        await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_EDIT_NOTES])
        service.delete(note.id)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.get(f"{WebConfig.ROUTE_PREFIX}/get-notes", status_code=HTTP_200_OK, response_model=NoteListResponse)
async def get_all_notes(request: Request, introspection_facade: IntrospectionFacade = Depends(),
                        service: NoteService = Depends()):
    try:
        owner = await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_READ_NOTES])
        notes = service.get_notes(owner)
        note_list_response = []
        for note in notes:
            note_list_response.append(NoteResponse(id=note.id, owner=note.owner, lastEdition=note.last_edition,
                                                   title=note.title, content=note.content))
        return NoteListResponse(notes=note_list_response)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
