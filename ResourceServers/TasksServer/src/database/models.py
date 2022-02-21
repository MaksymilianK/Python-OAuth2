import logging

from sqlalchemy import Column, Integer, String, Boolean

from config import DBConfig
from . import Base, engine


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String, nullable=False)
    day = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    owner = Column(String, index=True, nullable=False)


Base.metadata.create_all(engine)

logging.info(f"Initialize database '{DBConfig.NAME}'")
