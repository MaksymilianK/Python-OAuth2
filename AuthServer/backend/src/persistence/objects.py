from typing import Optional, List
from datetime import datetime


class User:
    def __init__(self, nick: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None):
        self.nick = nick
        self.email = email
        self.password = password

    def __repr__(self):
        text = ''

        if self.nick is not None:
            text += f'nick: {self.nick}, '
        if self.email is not None:
            text += f'email: {self.email}, '
        if self.password is not None:
            text += f'password hash: {self.password}'

        return text


class Client:
    def __init__(self, id: Optional[int] = None, name: Optional[str] = None, description: Optional[str] = None,
                 redirect_url: Optional[str] = None, owner_nick: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description
        self.redirect_url = redirect_url
        self.owner_nick = owner_nick

    def __repr__(self):
        text = ''

        if self.id is not None:
            text += f'id: {self.id}, '
        if self.name is not None:
            text += f'name: {self.name}, '
        if self.description is not None:
            text += f'description: {self.description}, '
        if self.redirect_url is not None:
            text += f'redirect url: {self.redirect_url}, '
        if self.owner_nick is not None:
            text += f'owner: {self.owner_nick}'

        return text


class Session:
    def __init__(self, id: Optional[str] = None, owner_nick: Optional[str] = None, date: Optional[datetime] = None):
        self.id = id
        self.owner_nick = owner_nick
        self.date = date

    def __repr__(self):
        text = ''

        if self.id is not None:
            text += f'id: {self.id}, '
        if self.owner_nick is not None:
            text += f'owner: {self.owner_nick}, '
        if self.date is not None:
            text += f'date: {self.date.strftime("%Y-%m-%d %H:%M:%S")}'

        return text


class AuthToken:
    def __init__(self, token: Optional[str] = None, owner_nick: Optional[str] = None, client_id: Optional[int] = None,
                 scope: Optional[List[str]] = None, date: Optional[datetime] = None):
        self.token = token
        self.owner_nick = owner_nick
        self.client_id = client_id
        self.scope = scope
        self.date = date

    def __repr__(self):
        text = ''

        if self.token is not None:
            text += f'token: {self.token}, '
        if self.owner_nick is not None:
            text += f'owner: {self.owner_nick}, '
        if self.client_id is not None:
            text += f'client: {self.client_id}, '
        if self.scope is not None:
            text += f'scope: {self.scope}, '
        if self.date is not None:
            text += f'date: {self.date.strftime("%Y-%m-%d %H:%M:%S")}'

        return text


class AuthCodeInfo:
    def __init__(self, code: Optional[str] = None, client_id: Optional[int] = None, scope: Optional[List[str]] = None,
                 owner_nick: Optional[str] = None):
        self.code = code
        self.client_id = client_id
        self.scope = scope
        self.owner_nick = owner_nick

    def __repr__(self):
        text = ''

        if self.code is not None:
            text += f'code: {self.code}, '
        if self.client_id is not None:
            text += f'client: {self.client_id}, '
        if self.scope is not None:
            text += f'scope: {self.scope}, '
        if self.owner_nick is not None:
            text += f'owner: {self.owner_nick}'

        return text


class SavedScope:
    def __init__(self, user_nick: Optional[str] = None, client_id: Optional[int] = None,
                 scope: Optional[List[str]] = None):
        self.user_nick = user_nick
        self.client_id = client_id
        self.scope = scope

    def __repr__(self):
        text = ''

        if self.user_nick is not None:
            text += f'user: {self.user_nick}, '
        if self.client_id is not None:
            text += f'client: {self.client_id}, '
        if self.scope is not None:
            text += f'scope: {self.scope}'

        return text
