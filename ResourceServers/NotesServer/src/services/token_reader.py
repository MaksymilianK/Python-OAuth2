from typing import Optional

from starlette.requests import Request


class TokenReader:
    def read_token(self, request: Request) -> Optional[str]:
        auth_token = request.headers["Authorization"]
        return auth_token
