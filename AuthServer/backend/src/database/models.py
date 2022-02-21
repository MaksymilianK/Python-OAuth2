from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY, DateTime

from . import Base, engine

import logging

from config import DBConfig


class UserModel(Base):
    __tablename__ = "users"

    nick = Column(String, primary_key=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)


class ClientModel(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    redirect_url = Column(String, nullable=False)
    owner_nick = Column(String, ForeignKey("users.nick"))


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, nullable=False)
    owner_nick = Column(String, ForeignKey("users.nick"), index=True)
    date = Column(DateTime, index=True, nullable=False)


class TokenModel(Base):
    __tablename__ = "tokens"

    token_id = Column(String, primary_key=True, nullable=False)
    owner_nick = Column(String, ForeignKey("users.nick"), index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    scopes = Column(ARRAY(String))
    date = Column(DateTime, index=True, nullable=False)


class SavedScopeModel(Base):
    __tablename__ = "saved_scopes"

    user_nick = Column(String, ForeignKey("users.nick"), primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), primary_key=True)
    scopes = Column(ARRAY(String))


Base.metadata.create_all(engine)

logging.info(f"Initialize database '{DBConfig.NAME}'")
