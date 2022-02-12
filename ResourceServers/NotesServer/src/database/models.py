from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from . import Base


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    owner = Column(String, index=True, nullable=False)
    last_edition = Column(DateTime, index=True, nullable=False)


class UserModel(Base):
    __tablename__ = "users"

    nick = Column(String, primary_key=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
