from typing import Optional


class User:
    def __init__(self, nick: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None):
        self.nick = nick
        self.email = email
        self.password = password


class Client:
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None, redirect_url: Optional[str] = None,
                 owner: Optional[User] = None):
        self.name = name
        self.description = description
        self.redirect_url = redirect_url
        self.owner = owner


class Session:
    def __init__(self, id: Optional[str] = None, owner: Optional[User] = None):
        self.id = id
        self.owner = owner

