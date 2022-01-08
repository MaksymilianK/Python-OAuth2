from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.database import engine, Base
from src.exceptions import ClientNotAuthenticatedException, ClientNotAuthorizedException
from src.handler.schemas import NoteCreateRequest, NoteIdResponse, NoteResponse
from src.services.introspection_fasade import IntrospectionFacade
from src.services.note_service import NoteService

Base.metadata.create_all(bind=engine)

app = FastAPI()

SCOPE_READ_NOTES = "NOTES_READ"
SCOPE_CREATE_NOTES = "NOTES_CREATE"
SCOPE_EDIT_NOTES = "NOTES_EDIT"


@app.post("/my-notes/api/notes", status_code=HTTP_201_CREATED, response_model=NoteIdResponse)
async def create_note(request: Request, note: NoteCreateRequest,
                  introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                  service: NoteService = Depends(NoteService)):
    try:
        owner = await introspection_facade.check_auth(request, [SCOPE_CREATE_NOTES])
        return service.create(note, owner)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.get("/my-notes/api/notes/{note_id}", status_code=HTTP_200_OK, response_model=NoteResponse)
async def get_one_note(request: Request, note_id: int,
                  introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                  service: NoteService = Depends(NoteService)):
    try:
        owner = await introspection_facade.check_auth(request, [SCOPE_READ_NOTES])
        return service.get(owner, )
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
