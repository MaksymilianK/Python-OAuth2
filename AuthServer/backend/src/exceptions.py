class NickExistsException(Exception):
    detail = 1
    pass


class EmailExistsException(Exception):
    detail = 2
    pass


class EmailNotExistException(Exception):
    detail = 3
    pass


class WrongPasswordException(Exception):
    detail = 4
    pass


class UserNotAuthenticatedException(Exception):
    detail = 5
    pass


class ClientNameExistsException(Exception):
    detail = 6
    pass


class ClientRedirectURLExistsException(Exception):
    detail = 7
    pass


class ClientNotFoundException(Exception):
    detail = 8
    pass


class AuthCodeNotFoundException(Exception):
    detail = 9
    pass


class TokenNotFoundException(Exception):
    detail = 10
    pass
