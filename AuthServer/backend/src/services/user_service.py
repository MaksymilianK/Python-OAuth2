import logging

from fastapi import Depends
from typing import Tuple

from web.schemas import UserCreateRequest, UserSignInRequest
from persistence.objects import User
from persistence.user_dao import UserDAO
from exceptions import NickExistsException, EmailExistsException, EmailNotExistException, WrongPasswordException, \
    UserNotAuthenticatedException
from services.password_service import PasswordService
from services.session_service import SessionService


class UserService:
    def __init__(self, password_service: PasswordService = Depends(), session_service: SessionService = Depends(),
                 dao: UserDAO = Depends()):
        self.__password_service = password_service
        self.__session_service = session_service
        self.__dao = dao

    def create(self, user_request: UserCreateRequest) -> Tuple[User, str]:
        if self.__dao.exists_with_nick(user_request.nick):
            raise NickExistsException()
        elif self.__dao.exists_with_email(user_request.email):
            raise EmailExistsException()

        user = User(
            nick=user_request.nick,
            email=user_request.email,
            password=self.__password_service.generate_hash(user_request.password)
        )

        self.__dao.create(user)

        logging.info(f"User '{user.nick}' signed up")

        return user, self.__session_service.create(user)

    def sign_in(self, form: UserSignInRequest) -> Tuple[User, str]:
        user = self.__dao.get_one_by_email(form.email)
        if user is None:
            raise EmailNotExistException()

        if not self.__password_service.verify(user.password, form.password):
            raise WrongPasswordException()

        session_id = self.__session_service.create(user)

        logging.info(f"User '{user.nick}' signed in with session id '{session_id}'")

        return user, session_id

    def sign_out(self, session_id: str):
        self.__session_service.delete(session_id)

        logging.info(f"User with session id '{session_id}' signed out")

    def get_user(self, session_id: str) -> User:
        user = self.__session_service.get_user(session_id)
        if user is None:
            raise UserNotAuthenticatedException()

        return user
