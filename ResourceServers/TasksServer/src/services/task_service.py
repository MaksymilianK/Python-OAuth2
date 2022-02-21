import logging

from fastapi import Depends

from web.schemas import TaskCreateRequest, TaskRequest
from persistence.task_dao import TaskDAO
from persistence.objects import Task
from services.introspection_fasade import IntrospectionFacade


class TaskService:
    def __init__(self, introspection_facade: IntrospectionFacade = Depends(), dao: TaskDAO = Depends()):
        self.__introspection_facade = introspection_facade
        self.__dao = dao

    def create(self, task_request: TaskCreateRequest, owner: str) -> Task:
        task = Task(
            text=task_request.text,
            day=task_request.day,
            status=task_request.status,
            owner=owner
        )

        task.id = self.__dao.create(task)

        logging.info(f"Create task with id {task.id}")

        return task

    def get_all(self, owner: str) -> list[Task]:
        return self.__dao.get_all(owner)

    def get_one(self, task_id: int) -> Task:
        return self.__dao.get_one(task_id)

    def delete(self, task_id: int):
        self.__dao.delete(task_id)

        logging.info(f"Delete task with id {task_id}")

    def update_status(self, task_id: int, task_request: TaskRequest) -> Task:
        task = self.__dao.update_status(task_id, task_request.status)

        logging.info(f"Update status of the task with id {task_id}")

        return task


