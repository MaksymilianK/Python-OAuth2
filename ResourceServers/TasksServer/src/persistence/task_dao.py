from fastapi import Depends

from database import SessionLocal, get_db
from database.models import TaskModel
from persistence.objects import Task


class TaskDAO:
    def __init__(self, db: SessionLocal = Depends(get_db)):
        self.__db = db

    def create(self, task: Task) -> int:
        task_model = TaskModel(text=task.text, day=task.day, status=task.status, owner=task.owner)
        self.__db.add(task_model)
        self.__db.commit()

        self.__db.refresh(task_model)
        return task_model.id

    def get_all(self, owner: str) -> list[Task]:
        tasks = self.__db.query(TaskModel).filter(TaskModel.owner == owner).all()
        if tasks is None:
            return []
        return [Task(t.id, t.text, t.day, t.status, t.owner) for t in tasks]

    def get_one(self, task_id: int) -> Task:
        task_model = self.__db.query(TaskModel).filter(TaskModel.id == task_id).one()
        return Task(task_model.id, task_model.text, task_model.day, task_model.status, task_model.owner)

    def delete(self, task_id: int):
        self.__db.query(TaskModel).filter(TaskModel.id == task_id).delete()
        self.__db.commit()

    def update_status(self, task_id: int, new_status: bool) -> Task:
        task_model = self.__db.query(TaskModel).filter(TaskModel.id == task_id).one()

        task_model.status = new_status
        self.__db.commit()

        return Task(task_model.id, task_model.text, task_model.day, task_model.status, task_model.owner)
