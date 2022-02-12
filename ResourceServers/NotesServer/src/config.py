class DBConfig:
    USER = 'my_admin'
    PASS = 'Jm08sf68SA13nBsd12'
    HOST = '185.218.125.97'
    PORT = 5432
    NAME = 'my_notes'


class WebConfig:
    ROUTE_PREFIX = "/my-notes/api"
    CORS_ENABLED = False
    CORS_ORIGINS = ["http://185.218.125.97:8081"]


class OAuth2Config:
    SCOPE_READ_NOTES = "NOTES_READ"
    SCOPE_CREATE_NOTES = "NOTES_CREATE"
    SCOPE_EDIT_NOTES = "NOTES_EDIT"
