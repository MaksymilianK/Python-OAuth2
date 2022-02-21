import logging

from fastapi import Depends
from starlette.requests import Request
from typing import List

from exceptions import ClientNotAuthorizedException, ClientNotAuthenticatedException
from services.introspection_service import IntrospectionService
from services.scope_checker import ScopeChecker
from services.token_reader import TokenReader


class IntrospectionFacade:
    def __init__(self, token_reader: TokenReader = Depends(), service: IntrospectionService = Depends(),
                 scope_checker: ScopeChecker = Depends()):
        self.__token_reader = token_reader
        self.__service = service
        self.__scope_checker = scope_checker

    async def check_auth(self, request: Request, required_scopes: List[str]) -> str:
        token = self.__token_reader.read_token(request)
        if token is None:
            raise ClientNotAuthenticatedException()

        token_info = await self.__service.get_token_info(token)
        if token_info is None or not token_info.active:
            raise ClientNotAuthenticatedException()

        if not self.__scope_checker.has_scopes(token_info, required_scopes):
            raise ClientNotAuthorizedException()

        logging.info(f"Checking authorization for owner '{token_info.owner}' & client id {token_info.client_id}")

        return token_info.owner
