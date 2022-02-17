from persistence.objects import AuthToken
from persistence.token_dao import TokenDAO

from datetime import datetime


class AdminService:
    def __init__(self, token_dao: TokenDAO):
        self.__token_dao = token_dao

    def get_all_active(self, nick: str) -> list[AuthToken]:
        return self.__token_dao.get_all_before(datetime.now(), nick)

    def revoke(self, token: str):
        self.__token_dao.update_date(token, datetime.now())
