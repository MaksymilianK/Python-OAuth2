from typing import Optional

from src.persistence.objects import AuthCodeInfo


AUTH_CODES_INFO: dict[str, AuthCodeInfo] = None


class AuthCodeDAO:
    def __init__(self):
        global AUTH_CODES_INFO
        if AUTH_CODES_INFO is None:
            print("init")
            AUTH_CODES_INFO = {}

        self.__auth_codes_info = AUTH_CODES_INFO

    def store(self, auth_code_info: AuthCodeInfo):
        print("code store", auth_code_info.code)
        self.__auth_codes_info[auth_code_info.code] = auth_code_info

    def get(self, code: str) -> Optional[AuthCodeInfo]:
        print("code get", code)
        return self.__auth_codes_info.get(code)
