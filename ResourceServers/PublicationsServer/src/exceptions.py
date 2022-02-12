class ClientNotAuthenticatedException(Exception):
    detail = 5
    pass


class ClientNotAuthorizedException(Exception):
    detail = 8
    pass
