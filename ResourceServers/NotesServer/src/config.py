class DBConfig:
    USER = 'my_admin'
    PASS = 'password'
    HOST = 'localhost'
    PORT = 5432
    NAME = 'my_notes'


class WebConfig:
    ROUTE_PREFIX = "/my-notes/api"
    CORS_ENABLED = False
    CORS_ORIGINS = ["http://localhost:8081"]


class OAuth2Config:
    INTROSPECTION_ENDPOINT = "http://localhost/my-auth/api/token-info"
    SCOPE_READ_NOTES = "NOTES_READ"
    SCOPE_CREATE_NOTES = "NOTES_CREATE"
    SCOPE_EDIT_NOTES = "NOTES_EDIT"
