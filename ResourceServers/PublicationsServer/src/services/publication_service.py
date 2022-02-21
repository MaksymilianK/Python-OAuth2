import logging
from datetime import datetime
from typing import List

from fastapi import Depends

from web.schemas import PublicationCreateRequest, PublicationEditRequest
from persistence.objects import Publication
from persistence.publication_dao import PublicationDAO
from services.introspection_fasade import IntrospectionFacade


class PublicationService:
    def __init__(self, introspection_facade: IntrospectionFacade = Depends(), dao: PublicationDAO = Depends()):
        self.__introspection_facade = introspection_facade
        self.__dao = dao

    def create(self, publication_request: PublicationCreateRequest, owner: str) -> Publication:
        publication = Publication(
            content=publication_request.content,
            owner=owner,
            create_time=datetime.now(),
            last_edition=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        publication.id = self.__dao.create(publication)

        logging.info(f"Create publication with id {publication.id}")

        return publication

    def delete(self, publication_id: int):
        self.__dao.delete(publication_id)

        logging.info(f"Delete publication with id {publication_id}")

    def get_publications(self) -> List[Publication]:
        return self.__dao.get_all()

    def edit(self, publication_request: PublicationEditRequest, owner: str) -> Publication:
        publication = self.__dao.edit(publication_request.id, publication_request.content, owner)

        logging.info(f"Edit publication with id {publication_request.id}")

        return publication
