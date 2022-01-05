from fastapi import Depends

from src.handler.schemas import UserCreateRequest, UserSignInRequest
from src.persistence.objects import User
from src.persistence.user_dao import UserDAO
from src.exceptions import NickExistsException, EmailExistsException, EmailNotExistException, WrongPasswordException, \
    UserNotAuthenticatedException
from src.services.password_service import PasswordService
from src.services.session_service import SessionService


class UserService:
    def __init__(self, password_service: PasswordService = Depends(PasswordService),
                 session_service: SessionService = Depends(SessionService),
                 dao: UserDAO = Depends(UserDAO)):
        self.__password_service = password_service
        self.__session_service = session_service
        self.__dao = dao

    def create_user(self, user: UserCreateRequest) -> str:
        if self.__dao.exists_with_nick(user.nick):
            raise NickExistsException()
        elif self.__dao.exists_with_email(user.email):
            raise EmailExistsException()

        user_with_hash = User(
            nick=user.nick,
            email=user.email,
            password=self.__password_service.generate_hash(user.password)
        )

        self.__dao.create(user_with_hash)
        return self.__session_service.create(user_with_hash)

    def sign_in(self, form: UserSignInRequest) -> str:
        user = self.__dao.get_one_by_email(form.email)
        if user is None:
            raise EmailNotExistException()

        if not self.__password_service.verify(user.password, form.password):
            raise WrongPasswordException()

        return self.__session_service.create(user)

    def sign_out(self, session_id: str):
        self.__session_service.delete(session_id)

    def get_user(self, session_id: str) -> User:
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        return user
