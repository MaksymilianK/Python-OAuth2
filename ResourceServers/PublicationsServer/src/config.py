class DBConfig:
    USER = 'my_admin'
    PASS = 'password'
    HOST = 'localhost'
    PORT = 5432
    NAME = 'my_publications'


class WebConfig:
    ROUTE_PREFIX = "/my-publications/api"
    CORS_ENABLED = False
    CORS_ORIGINS = ["http://localhost:8082"]


class OAuth2Config:
    INTROSPECTION_ENDPOINT = "http://localhost/my-auth/api/token-info"
    SCOPE_READ_PUBLICATIONS = "PUBLICATIONS_READ"
    SCOPE_CREATE_PUBLICATIONS = "PUBLICATIONS_CREATE"
    SCOPE_EDIT_PUBLICATIONS = "PUBLICATIONS_EDIT"
