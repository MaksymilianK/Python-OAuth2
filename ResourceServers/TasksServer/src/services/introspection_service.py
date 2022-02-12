from typing import Optional

import httpx

from persistence.objects import AuthTokenInfo


INTROSPECTION_ENDPOINT = "http://localhost:8000/my-auth/api/token-info"


class IntrospectionService:
    async def get_token_info(self, token: str) -> Optional[AuthTokenInfo]:
        async with httpx.AsyncClient() as client:
            request_body = {"token": token}
            response = await client.post(INTROSPECTION_ENDPOINT, json=request_body)
            response_body = response.json()

            return AuthTokenInfo(response_body["owner"], response_body["clientId"], response_body["scopes"])
