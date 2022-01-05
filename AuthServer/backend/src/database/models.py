from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


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


class AuthTokenModel(Base):
    __tablename__ = "auth_tokens"

    id = Column(String, primary_key=True, nullable=False)
    owner_nick = Column(String, ForeignKey("users.nick"), index=True)
    clientName = Column(String, ForeignKey("clients.name"), index=True)
