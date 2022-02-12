from sqlalchemy import Column, Integer, String, Boolean

from . import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String, nullable=False)
    day = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    owner = Column(String, index=True, nullable=False)


class UserModel(Base):
    __tablename__ = "users"

    nick = Column(String, primary_key=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
