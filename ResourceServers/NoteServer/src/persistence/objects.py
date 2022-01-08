from datetime import datetime
from typing import Optional


class Note:
    def __init__(self, id: Optional[int] = None, title: Optional[str] = None, content: Optional[str] = None,
                 owner: Optional[str] = None, last_edition: Optional[datetime] = None):
        self.id = id
        self.title = title
        self.content = content
        self.owner = owner
        self.last_edition = last_edition


class AuthTokenInfo:
    def __init__(self, owner: str, client_id: int, scopes: list[str]):
        self.owner = owner
        self.client_id = client_id
        self.scopes = scopes
