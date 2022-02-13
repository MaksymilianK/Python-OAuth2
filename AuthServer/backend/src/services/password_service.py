from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Depends


class PasswordService:
    def __init__(self, password_hasher: PasswordHasher = Depends()):
        self.__password_hasher = password_hasher

    def generate_hash(self, password: str):
        return self.__password_hasher.hash(password)

    def verify(self, password_hash: str, password: str):
        try:
            self.__password_hasher.verify(password_hash, password)
        except VerificationError:
            return False

        return True
