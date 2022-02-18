from datetime import datetime
from typing import Optional, List


class Publication:
    def __init__(self, id: Optional[int] = None,  content: Optional[str] = None, owner: Optional[str] = None,
                 last_edition: Optional[str] = None, create_time: Optional[datetime] = None):
        self.id = id
        self.content = content
        self.owner = owner
        self.last_edition = last_edition
        self.create_time = create_time

    def __repr__(self):
        text = ''

        if self.id is not None:
            text += f'id: {self.id}, '
        if self.content is not None:
            text += f'content: {self.content}, '
        if self.owner is not None:
            text += f'owner: {self.owner}, '
        if self.last_edition is not None:
            text += f'last edition: {self.last_edition}, '
        if self.create_time is not None:
            text += f'create time: {self.create_time.strftime("%Y-%m-%d %H:%M:%S")}'

        return text


class AuthTokenInfo:
    def __init__(self, owner: str, client_id: int, scopes: List[str], active: bool):
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
