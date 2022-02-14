from fastapi import Depends, FastAPI, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from database import engine, Base
from exceptions import ClientNotAuthenticatedException, ClientNotAuthorizedException
from web.schemas import TaskCreateRequest, TaskRequest, TaskCreateResponse, TaskResponse, TaskListResponse, \
    TaskUpdateStatusResponse
from services.introspection_fasade import IntrospectionFacade
from services.task_service import TaskService

from config import WebConfig, OAuth2Config

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post(WebConfig.ROUTE_PREFIX + '/tasks', status_code=HTTP_201_CREATED, response_model=TaskCreateResponse)
async def create_task(request: Request, task: TaskCreateRequest, introspection_facade: IntrospectionFacade = Depends(),
                      service: TaskService = Depends()):
    try:
        owner = await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_CREATE_TASKS])
        res = service.create(task, owner)

        return TaskCreateResponse(id=res.id, text=res.text, day=res.day, status=res.status)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.get(WebConfig.ROUTE_PREFIX + '/tasks', status_code=HTTP_200_OK, response_model=TaskListResponse)
async def get_tasks(request: Request, introspection_facade: IntrospectionFacade = Depends(),
                    service: TaskService = Depends()):
    try:
        owner = await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_READ_TASKS])
        tasks = service.get_all(owner)

        res = []
        for task in tasks:
            res.append(TaskResponse(id=task.id, text=task.text, day=task.day, status=task.status))

        return TaskListResponse(tasks=res)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.get(WebConfig.ROUTE_PREFIX + '/tasks/{task_id}', status_code=HTTP_200_OK, response_model=TaskResponse)
async def get_one_task(request: Request, task_id: int, introspection_facade: IntrospectionFacade = Depends(),
                       service: TaskService = Depends()):
    try:
        await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_READ_TASKS])
        res = service.get_one(task_id)

        return TaskResponse(id=res.id, text=res.text, day=res.day, status=res.status)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.delete(WebConfig.ROUTE_PREFIX + '/tasks/{task_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_task(request: Request, task_id: int, introspection_facade: IntrospectionFacade = Depends(),
                      service: TaskService = Depends()):
    try:
        await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_EDIT_TASKS])
        service.delete(task_id)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@app.put(WebConfig.ROUTE_PREFIX + '/tasks/{task_id}', status_code=HTTP_200_OK, response_model=TaskUpdateStatusResponse)
async def update_task_status(request: Request, task_id: int, task: TaskRequest,
                             introspection_facade: IntrospectionFacade = Depends(),
                             service: TaskService = Depends()):
    try:
        await introspection_facade.check_auth(request, [OAuth2Config.SCOPE_EDIT_TASKS])
        res = service.update_status(task_id, task)

        return TaskUpdateStatusResponse(status=res.status)
    except ClientNotAuthenticatedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except ClientNotAuthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
