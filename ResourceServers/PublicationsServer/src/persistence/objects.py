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


class AuthTokenInfo:
    def __init__(self, owner: str, client_id: int, scopes: List[str], active: bool):
        self.owner = owner
        self.client_id = client_id
        self.scopes = scopes
        self.active = active
