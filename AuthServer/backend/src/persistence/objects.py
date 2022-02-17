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
    def __init__(self, id: Optional[str] = None, owner: Optional[User] = None, date: Optional[datetime] = None):
        self.id = id
        self.owner = owner
        self.date = date


class AuthToken:
    def __init__(self, token: Optional[str] = None, owner: Optional[User] = None, client: Optional[Client] = None,
                 scope: Optional[List[str]] = None, date: Optional[datetime] = None):
        self.token = token
        self.owner = owner
        self.client = client
        self.scope = scope
        self.date = date

    def __repr__(self):
        text = ''

        if self.token is not None:
            text += f'token: {self.token}, '
        if self.owner is not None:
            text += f'owner: {self.owner}, '
        if self.client is not None:
            text += f'client: {self.client}, '
        if self.scope is not None:
            text += f'scope: {self.scope}, '
        if self.date is not None:
            text += f'date: {self.date.strftime("%Y-%m-%d %H:%M:%S")}'

        return text


class AuthCodeInfo:
    def __init__(self, code: Optional[str] = None, client: Optional[Client] = None, scope: Optional[List[str]] = None,
                 owner: Optional[User] = None):
        self.code = code
        self.client = client
        self.scope = scope
        self.owner = owner
