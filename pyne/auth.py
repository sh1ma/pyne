"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from typing import Dict

from frugal.context import FContext

from .api import Api, ApiFactory
from .line_thrift.line import FAuthServiceClient, LoginRequest, LoginResult


class AuthApi(Api, FAuthServiceClient):
    """AuthServiceのApiクラス

    """

    async def login(self, login_request: LoginRequest) -> LoginResult:
        await self.loginZ(FContext(), login_request)

class AuthApiFactory(ApiFactory):
    """`AuthApi`のファクトリクラス

    """

    def create(self, path: str, headers: Dict) -> AuthApi:
        provider = self.get_provider(path, headers)
        return AuthApi(provider)
