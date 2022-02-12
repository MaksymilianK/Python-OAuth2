from typing import Optional


class Task:
    def __init__(self, id: Optional[int] = None, text: Optional[str] = None, day: Optional[str] = None,
                 status: Optional[bool] = None, owner: Optional[str] = None):
        self.id = id
        self.text = text
        self.day = day
        self.status = status
        self.owner = owner


class AuthTokenInfo:
    def __init__(self, owner: str, client_id: int, scopes: list[str]):
        self.owner = owner
        self.client_id = client_id
        self.scopes = scopes


class User:
    def __init__(self, nick: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None):
        self.nick = nick
        self.email = email
        self.password = password