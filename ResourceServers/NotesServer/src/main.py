from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from database import engine, Base
from exceptions import ClientNotAuthenticatedException, ClientNotAuthorizedException
from handler.schemas import NoteCreateRequest, NoteResponse, NoteListResponse, NoteCreateResponse, NoteDeleteRequest
from services.introspection_fasade import IntrospectionFacade
from services.note_service import NoteService
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8081",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SCOPE_READ_NOTES = "NOTES_READ"
SCOPE_CREATE_NOTES = "NOTES_CREATE"
SCOPE_EDIT_NOTES = "NOTES_EDIT"


@app.post("/my-notes/api/add-note", status_code=HTTP_201_CREATED, response_model=NoteCreateResponse)
async def create_note(request: Request, note: NoteCreateRequest,
                      introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                      service: NoteService = Depends(NoteService)):
    try:
        owner = await introspection_facade.check_auth(request, [SCOPE_CREATE_NOTES])
        note_create_response = service.create(note, owner)
        return NoteCreateResponse(id=note_create_response.id, lastEdition=note_create_response.last_edition)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.delete("/my-notes/api/delete-note", status_code=HTTP_204_NO_CONTENT)
async def delete_note(request: Request, note: NoteDeleteRequest,
                      introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                      service: NoteService = Depends(NoteService)):
    try:
        await introspection_facade.check_auth(request, [SCOPE_EDIT_NOTES])
        service.delete(note.id)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.get("/my-notes/api/get-notes", status_code=HTTP_200_OK, response_model=NoteListResponse)
async def get_all_notes(request: Request,
                        introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                        service: NoteService = Depends(NoteService)):
    try:
        owner = await introspection_facade.check_auth(request, [SCOPE_READ_NOTES])
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
