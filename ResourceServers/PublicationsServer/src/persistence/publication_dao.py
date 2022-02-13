from datetime import datetime
from typing import Optional, List

from fastapi import Depends

from database.models import PublicationModel
from persistence.objects import Publication
from database import SessionLocal, get_db


class PublicationDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def create(self, publication: Publication) -> int:
        publication_model = PublicationModel(content=publication.content, owner=publication.owner,
                                             last_edition=publication.last_edition, create_time=publication.create_time)
        self.__db.add(publication_model)
        self.__db.commit()

        self.__db.refresh(publication_model)
        return publication_model.id

    def delete(self, publication_id: int):
        self.__db.query(PublicationModel).filter(PublicationModel.id == publication_id).delete()
        self.__db.commit()

    def get_all(self) -> List[Publication]:
        publications = self.__db.query(PublicationModel).order_by(PublicationModel.create_time).all()
        if publications is None:
            return []
        return [Publication(p.id, p.content, p.owner, p.last_edition, p.create_time) for p in publications]

    def edit(self, publication_id: int, content: str, owner: str):
        publication = self.__db.query(PublicationModel).filter(PublicationModel.id == publication_id and
                                                               PublicationModel.owner == owner).first()
        publication.content = content
        publication.last_edition = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " edited"
        self.__db.commit()
        self.__db.refresh(publication)
        return publication

