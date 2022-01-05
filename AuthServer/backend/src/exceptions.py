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
