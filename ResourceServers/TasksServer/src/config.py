class DBConfig:
    USER = 'my_admin'
    PASS = 'Jm08sf68SA13nBsd12'
    HOST = '185.218.125.97'
    PORT = 5432
    NAME = 'my_tasks'


class WebConfig:
    ROUTE_PREFIX = "/my-tasks/api"
    CORS_ENABLED = False
    CORS_ORIGINS = ["http://185.218.125.97:8083"]


class OAuth2Config:
    INTROSPECTION_ENDPOINT = "http://185.218.125.97/my-auth/api/token-info"
    SCOPE_READ_TASKS = "TASKS_READ"
    SCOPE_CREATE_TASKS = "TASKS_CREATE"
    SCOPE_EDIT_TASKS = "TASKS_EDIT"
