class ClientNotAuthenticatedException(Exception):
    detail = 1
    pass


class ClientNotAuthorizedException(Exception):
    detail = 2
    pass
