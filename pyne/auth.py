"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from typing import Dict

from .api import Api, ApiFactory
from .line_thrift.line import FAuthServiceClient
from .line_thrift.line import LoginResult, LoginRequest

from frugal.context import FContext

class AuthApi(Api, FAuthServiceClient):
    """AuthServiceのApiクラス

    """

    async def login(self, login_request: LoginRequest) -> LoginResult:
        login_result: LoginResult = await self.loginZ(FContext(), login_request)

        return login_result

class AuthApiFactory(ApiFactory):
    """`AuthApi`のファクトリクラス

    """

    def create(self, path: str, headers: Dict) -> AuthApi:
        provider = self.get_provider(path, headers)
        return AuthApi(provider)
