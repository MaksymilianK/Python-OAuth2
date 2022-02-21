import logging

from sqlalchemy import Column, Integer, String, DateTime

from config import DBConfig
from . import Base, engine


class PublicationModel(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    owner = Column(String, index=True, nullable=False)
    last_edition = Column(String, index=True, nullable=False)
    create_time = Column(DateTime, index=True, nullable=False)


Base.metadata.create_all(engine)

logging.info(f"Initialize database '{DBConfig.NAME}'")
