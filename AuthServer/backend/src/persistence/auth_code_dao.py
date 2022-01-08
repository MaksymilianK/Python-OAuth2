from typing import Optional

from src.persistence.objects import AuthCodeInfo


class AuthCodeDAO:
    def __init__(self):
        self.__auth_codes_info: dict[str, AuthCodeInfo] = {}

    def store(self, auth_code_info: AuthCodeInfo):
        self.__auth_codes_info[auth_code_info.code] = auth_code_info

    def get(self, code: str) -> Optional[AuthCodeInfo]:
        return self.__auth_codes_info.get(code)
