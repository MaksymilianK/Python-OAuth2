from typing import Optional, Dict

from .objects import AuthCodeInfo


AUTH_CODES_INFO: Dict[str, AuthCodeInfo] = None


class AuthCodeDAO:
    def __init__(self):
        global AUTH_CODES_INFO
        if AUTH_CODES_INFO is None:
            AUTH_CODES_INFO = {}

        self.__auth_codes_info = AUTH_CODES_INFO

    def store(self, auth_code_info: AuthCodeInfo):
        self.__auth_codes_info[auth_code_info.code] = auth_code_info

    def get(self, code: str) -> Optional[AuthCodeInfo]:
        return self.__auth_codes_info.get(code)

    def delete(self, code: str) -> bool:
        try:
            self.__auth_codes_info.pop(code)
            return True
        except KeyError:
            return False
