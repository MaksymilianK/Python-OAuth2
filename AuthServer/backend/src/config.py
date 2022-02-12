class DBConfig:
    USER = 'my_admin'
    PASS = 'Jm08sf68SA13nBsd12'
    HOST = '185.218.125.97'
    PORT = 5432
    NAME = 'my_auth'


class WebConfig:
    ROUTE_PREFIX = "/my-auth/api"
    CORS_ENABLED = False
    CORS_ORIGINS = [
        "http://185.218.125.97:8080",
        "http://185.218.125.97:8081",
        "http://185.218.125.97:8082",
        "http://185.218.125.97:8083"
    ]
