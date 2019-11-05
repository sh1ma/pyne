"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from abc import ABCMeta, abstractmethod
from typing import Dict

from frugal.provider import FServiceProvider
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory

from .http_client import HttpClientFactory
from .protocol import LineProtocolFactory


class Api(metaclass=ABCMeta):
    """Apiのメタクラス

    """


class ApiFactory(metaclass=ABCMeta):
    """Apiファクトリのメタクラス

    Attributes:
        host: APIホスト
    """

    def __init__(self, host: str):
        self.host = host

    @abstractmethod
    def create(self, path: str, headers: Dict):
        """Apiクラスを生成する関数

        Args:
            path: APIエンドポイントのpath
            headers: httpヘッダー
        """
        NotImplementedError()

    def get_provider(self, path, headers) -> FServiceProvider:
        """FServiceProviderクラスを生成する関数

        http clientとprotocol factoryを取得し、FServiceProviderに渡す。

        Args:
            path: APIエンドポイントのpath
            headers: httpヘッダー

        Return:
            `FServiceProvider`
        """
        http_client = HttpClientFactory(self.host).get_client(path, headers)
        protocol_factory = TCompactProtocolAcceleratedFactory()

        return FServiceProvider(http_client, LineProtocolFactory(protocol_factory))
