from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from web.schemas import PublicationCreateRequest, PublicationCreateResponse, \
    PublicationDeleteRequest, PublicationListResponse, PublicationResponse, PublicationEditResponse, \
    PublicationEditRequest
from services.publication_service import PublicationService
from database import engine, Base
from exceptions import ClientNotAuthenticatedException, ClientNotAuthorizedException
from services.introspection_fasade import IntrospectionFacade

from config import WebConfig, OAuth2Config

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post(f"{WebConfig.ROUTE_PREFIX}/add-publication", status_code=HTTP_201_CREATED, response_model=PublicationCreateResponse)
async def create_publication(request: Request, publication: PublicationCreateRequest,
                      introspection_facade: IntrospectionFacade = Depends(),
                      service: PublicationService = Depends()):
    try:
        owner = await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_CREATE_PUBLICATIONS])
        publication_create_response = service.create(publication, owner)
        return PublicationCreateResponse(id=publication_create_response.id, lastEdition=publication_create_response.last_edition)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.delete(f"{WebConfig.ROUTE_PREFIX}/delete-publication", status_code=HTTP_204_NO_CONTENT)
async def delete_publication(request: Request, publication: PublicationDeleteRequest,
                      introspection_facade: IntrospectionFacade = Depends(),
                      service: PublicationService = Depends()):
    try:
        await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_EDIT_PUBLICATIONS])
        service.delete(publication.id)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.get(f"{WebConfig.ROUTE_PREFIX}/get-publications", status_code=HTTP_200_OK, response_model=PublicationListResponse)
async def get_all_publications(request: Request, introspection_facade: IntrospectionFacade = Depends(),
                        service: PublicationService = Depends()):
    try:
        await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_READ_PUBLICATIONS])
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


@app.put(f"{WebConfig.ROUTE_PREFIX}/edit-publication", status_code=HTTP_200_OK, response_model=PublicationEditResponse)
async def edit_publication(request: Request, publication: PublicationEditRequest,
                      introspection_facade: IntrospectionFacade = Depends(),
                      service: PublicationService = Depends()):
    try:
        owner = await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_EDIT_PUBLICATIONS])
        publication_edit_response = service.edit(publication, owner)
        return PublicationEditResponse(lastEdition=publication_edit_response.last_edition)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
