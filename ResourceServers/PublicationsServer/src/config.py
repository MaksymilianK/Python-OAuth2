class DBConfig:
    USER = 'my_admin'
    PASS = 'Jm08sf68SA13nBsd12'
    HOST = '185.218.125.97'
    PORT = 5432
    NAME = 'my_publications'


class WebConfig:
    ROUTE_PREFIX = "/my-publications/api"
    CORS_ENABLED = False
    CORS_ORIGINS = ["http://185.218.125.97:8082"]


class OAuth2Config:
    SCOPE_READ_PUBLICATIONS = "PUBLICATIONS_READ"
    SCOPE_CREATE_PUBLICATIONS = "PUBLICATIONS_CREATE"
    SCOPE_EDIT_PUBLICATIONS = "PUBLICATIONS_EDIT"
