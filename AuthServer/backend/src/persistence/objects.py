from typing import Optional, List
from datetime import datetime


class User:
    def __init__(self, nick: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None):
        self.nick = nick
        self.email = email
        self.password = password


class Client:
    def __init__(self, id: Optional[int] = None, name: Optional[str] = None, description: Optional[str] = None,
                 redirect_url: Optional[str] = None, owner: Optional[User] = None):
        self.id = id
        self.name = name
        self.description = description
        self.redirect_url = redirect_url
        self.owner = owner


class Session:
    def __init__(self, id: Optional[str] = None, owner: Optional[User] = None):
        self.id = id
        self.owner = owner


class AuthToken:
    def __init__(self, token: Optional[str], owner: Optional[User], client: Optional[Client],
                 scope: Optional[List[str]], date: Optional[datetime]):
        self.token = token
        self.owner = owner
        self.client = client
        self.scope = scope
        self.date = date


class AuthCodeInfo:
    def __init__(self, code: Optional[str], client: Optional[Client], scope: Optional[List[str]],
                 owner: Optional[User]):
        self.code = code
        self.client = client
        self.scope = scope
        self.owner = owner
