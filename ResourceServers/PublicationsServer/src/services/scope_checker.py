from typing import List

from persistence.objects import AuthTokenInfo


class ScopeChecker:
    def has_scopes(self, token_info: AuthTokenInfo, required_scopes: List[str]) -> bool:
        for required_scopes in required_scopes:
            if required_scopes not in token_info.scopes:
                return False

        return True
