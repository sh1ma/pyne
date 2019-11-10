"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from typing import Dict

from .api import Api, ApiFactory
from .line_thrift.line import FTalkServiceClient
from .line_thrift.line import Profile
from .line_thrift.line import AuthQrcode

from frugal.context import FContext


class TalkApi(Api, FTalkServiceClient):
    """TalkServiceのApiクラス

    """

    async def get_profile(self) -> Profile:
        profile: Profile = await self.getProfile(FContext())
        return profile

    async def issue_qr_verifier(self, keep_logged_in: bool, system_name: str) -> str:
        qr_code: AuthQrcode = await self.getAuthQrcode(
            FContext(), keep_logged_in, system_name, False
        )
        return qr_code.verifier


class TalkApiFactory(ApiFactory):
    """`TalkApi`のファクトリクラス

    """

    def create(self, path: str, headers: Dict) -> TalkApi:
        provider = self.get_provider(path, headers)
        return TalkApi(provider)
