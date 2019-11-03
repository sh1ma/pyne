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
from .line_thrift.line import FAuthServiceClient, FTalkServiceClient
from .protocol import LineProtocolFactory


class Api(metaclass=ABCMeta):
    pass


class ApiFactory(metaclass=ABCMeta):
    def __init__(self, host: str):
        self.host = host

    @abstractmethod
    def create(self, path: str, headers: Dict):
        NotImplementedError()

    def get_provider(self, path, headers) -> FServiceProvider:
        http_client = HttpClientFactory(self.host).get_client(path, headers)
        protocol_factory = TCompactProtocolAcceleratedFactory()
        provider = FServiceProvider(http_client, LineProtocolFactory(protocol_factory))
        return provider


class TalkApi(Api, FTalkServiceClient):
    pass


class TalkApiFactory(ApiFactory):

    def create(self, path: str, headers: Dict) -> TalkApi:
        provider = self.get_provider(path, headers)
        return TalkApi(provider)


class AuthApi(Api, FAuthServiceClient):
    pass


class AuthApiFactory(ApiFactory):
    def create(self, path: str, headers: Dict) -> AuthApi:
        provider = self.get_provider(path, headers)
        return AuthApi(provider)
