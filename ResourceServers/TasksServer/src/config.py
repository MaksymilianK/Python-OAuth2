class DBConfig:
    USER = 'my_admin'
    PASS = 'password'
    HOST = 'localhost'
    PORT = 5432
    NAME = 'my_tasks'


class WebConfig:
    ROUTE_PREFIX = "/my-tasks/api"
    CORS_ENABLED = False
    CORS_ORIGINS = ["http://localhost:8083"]


class OAuth2Config:
    INTROSPECTION_ENDPOINT = "http://localhost/my-auth/api/token-info"
    SCOPE_READ_TASKS = "TASKS_READ"
    SCOPE_CREATE_TASKS = "TASKS_CREATE"
    SCOPE_EDIT_TASKS = "TASKS_EDIT"
