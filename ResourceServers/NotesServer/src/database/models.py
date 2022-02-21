import logging

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from config import DBConfig
from . import Base, engine


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    owner = Column(String, index=True, nullable=False)
    last_edition = Column(DateTime, index=True, nullable=False)


Base.metadata.create_all(engine)

logging.info(f"Initialize database '{DBConfig.NAME}'")
