from typing import Optional

from fastapi import Depends

from database import SessionLocal, get_db
from database.models import TaskModel, UserModel
from persistence.objects import Task, User


class TaskDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def exists_with_nick(self, nick: str) -> bool:
        return self.__db.query(UserModel).filter(UserModel.nick == nick).first() is not None

    def exists_with_email(self, email: str) -> bool:
        return self.__db.query(UserModel).filter(UserModel.email == email).first() is not None

    def get_one_by_email(self, email: str) -> Optional[User]:
        user = self.__db.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            return None

        return User(nick=user.nick, password=user.password_hash)

    def create(self, task: Task) -> int:
        task_model = TaskModel(text=task.text, day=task.day, status=task.status, owner=task.owner)
        self.__db.add(task_model)
        self.__db.commit()

        self.__db.refresh(task_model)
        return task_model.id

    def get_all(self, owner: str) -> list[TaskModel]:
        return self.__db.query(TaskModel).filter(TaskModel.owner == owner).all()

    def get(self, task_id: int) -> TaskModel:
        return self.__db.query(TaskModel).filter(TaskModel.id == task_id).one()

    def delete(self, task_id: int):
        self.__db.query(TaskModel).filter(TaskModel.id == task_id).delete()
        self.__db.commit()

    def update_status(self, task_id: int, task: Task) -> TaskModel:
        task_model = self.get(task_id)

        task_model.status = task.status
        self.__db.commit()

        return task_model
