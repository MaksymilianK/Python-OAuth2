from typing import Optional


class Task:
    def __init__(self, id: Optional[int] = None, text: Optional[str] = None, day: Optional[str] = None,
                 status: Optional[bool] = None, owner: Optional[str] = None):
        self.id = id
        self.text = text
        self.day = day
        self.status = status
        self.owner = owner

    def __repr__(self):
        text = ''

        if self.id is not None:
            text += f'id: {self.id}, '
        if self.text is not None:
            text += f'text: {self.text}, '
        if self.day is not None:
            text += f'day: {self.day}, '
        if self.status is not None:
            text += f'status: {self.status}, '
        if self.owner is not None:
            text += f'owner: {self.owner}'

        return text


class AuthTokenInfo:
    def __init__(self, owner: str, client_id: int, scopes: list[str], active: bool):
        self.owner = owner
        self.client_id = client_id
        self.scopes = scopes
        self.active = active

    def __repr__(self):
        text = ''

        if self.owner is not None:
            text += f'owner: {self.owner}, '
        if self.client_id is not None:
            text += f'client id: {self.client_id}, '
        if self.scopes is not None:
            text += f'scopes: {self.scopes}, '
        if self.active is not None:
            text += f'active: {self.active}'

        return text
