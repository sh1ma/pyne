"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from typing import Dict

from .api import Api, ApiFactory
from .line_thrift.line import FTalkServiceClient


class TalkApi(Api, FTalkServiceClient):
    """TalkServiceのApiクラス

    """


class TalkApiFactory(ApiFactory):
    """`TalkApi`のファクトリクラス

    """

    def create(self, path: str, headers: Dict) -> TalkApi:
        provider = self.get_provider(path, headers)
        return TalkApi(provider)
