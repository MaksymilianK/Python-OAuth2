class DBConfig:
    USER = 'my_admin'
    PASS = 'password'
    HOST = 'localhost'
    PORT = 5432
    NAME = 'my_auth'


class WebConfig:
    ROUTE_PREFIX = "/my-auth/api"
    CORS_ENABLED = False
    CORS_ORIGINS = [
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8082",
        "http://localhost:8083"
    ]


class OAuth2Config:
    AUTH_CODE_LIFETIME = 60
