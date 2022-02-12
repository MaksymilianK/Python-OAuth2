from fastapi import Depends

from web.schemas import TaskCreateRequest, TaskRequest
from persistence.task_dao import TaskDAO
from persistence.objects import Task
from services.introspection_fasade import IntrospectionFacade


class TaskService:
    def __init__(self, introspection_facade: IntrospectionFacade = Depends(IntrospectionFacade),
                 dao: TaskDAO = Depends(TaskDAO)):
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
        return task

    def get_all(self, owner: str) -> list[Task]:
        task_models = self.__dao.get_all(owner)

        tasks = []
        for task_model in task_models:
            task = Task(
                id=task_model.id,
                text=task_model.text,
                day=task_model.day,
                status=task_model.status,
            )
            tasks.append(task)

        return tasks

    def get(self, task_id: int) -> Task:
        task_model = self.__dao.get(task_id)

        task = Task(
            id=task_model.id,
            text=task_model.text,
            day=task_model.day,
            status=task_model.status,
        )
        return task

    def delete(self, task_id: int):
        self.__dao.delete(task_id)

    def update_status(self, task_id: int, task_request: TaskRequest) -> Task:
        task = Task(status=task_request.status)
        task_model = self.__dao.update_status(task_id, task)

        task.status = task_model.status

        return task
