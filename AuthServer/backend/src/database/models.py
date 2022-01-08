from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY

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


class TokenModel(Base):
    __tablename__ = "tokens"

    token_id = Column(String, primary_key=True, nullable=False)
    owner_nick = Column(String, ForeignKey("users.nick"), index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    scopes = Column(ARRAY(String))
