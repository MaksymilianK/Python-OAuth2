from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from handler.schemas import PublicationCreateRequest, PublicationCreateResponse, \
    PublicationDeleteRequest, PublicationListResponse, PublicationResponse, PublicationEditResponse, \
    PublicationEditRequest
from services.publication_service import PublicationService
from database import engine, Base
from exceptions import ClientNotAuthenticatedException, ClientNotAuthorizedException
from services.introspection_fasade import IntrospectionFacade
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8082",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPE_READ_PUBLICATIONS = "PUBLICATIONS_READ"
SCOPE_CREATE_PUBLICATIONS = "PUBLICATIONS_CREATE"
SCOPE_EDIT_PUBLICATIONS = "PUBLICATIONS_EDIT"

@app.post("/my-publications/api/add-publication", status_code=HTTP_201_CREATED, response_model=PublicationCreateResponse)
async def create_publication(request: Request, publication: PublicationCreateRequest,
                      introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                      service: PublicationService = Depends(PublicationService)):
    try:
        owner = await introspection_facade.check_auth(request, [SCOPE_CREATE_PUBLICATIONS])
        publication_create_response = service.create(publication, owner)
        return PublicationCreateResponse(id=publication_create_response.id, lastEdition=publication_create_response.last_edition)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.delete("/my-publications/api/delete-publication", status_code=HTTP_204_NO_CONTENT)
async def delete_publication(request: Request, publication: PublicationDeleteRequest,
                      introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                      service: PublicationService = Depends(PublicationService)):
    try:
        await introspection_facade.check_auth(request, [SCOPE_EDIT_PUBLICATIONS])
        service.delete(publication.id)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.get("/my-publications/api/get-publications", status_code=HTTP_200_OK, response_model=PublicationListResponse)
async def get_all_publications(request: Request,
                        introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                        service: PublicationService = Depends(PublicationService)):
    try:
        await introspection_facade.check_auth(request, [SCOPE_READ_PUBLICATIONS])
        publications = service.get_publications()
        publication_list_response = []
        for publication in publications:
            publication_list_response.append(PublicationResponse(id=publication.id, owner=publication.owner,
                                                                 lastEdition=publication.last_edition,
                                                                 content=publication.content))
        return PublicationListResponse(publications=publication_list_response)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.put("/my-publications/api/edit-publication", status_code=HTTP_200_OK, response_model=PublicationEditResponse)
async def edit_publication(request: Request, publication: PublicationEditRequest,
                      introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                      service: PublicationService = Depends(PublicationService)):
    try:
        owner = await introspection_facade.check_auth(request, [SCOPE_EDIT_PUBLICATIONS])
        publication_edit_response = service.edit(publication, owner)
        return PublicationEditResponse(lastEdition=publication_edit_response.last_edition)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)