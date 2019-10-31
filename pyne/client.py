# Copyright (c) 2019 4masaka
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABCMeta, abstractmethod
from typing import Dict

from frugal.protocol import FProtocolFactory
from frugal.provider import FServiceProvider
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory

from http_client import HttpClientFactory
from lib.line.f_AuthService import Client as Auth
from lib.line.f_TalkService import Client as Talk


class Client(metaclass=ABCMeta):
    pass


class ClientFactory(metaclass=ABCMeta):
    def __init__(self, host):
        self.host = host

    @abstractmethod
    def create(self, path: str, headers: Dict):
        NotImplementedError()

    def get_provider(self, path, headers):
        http_client = HttpClientFactory(self.host).get_client(path, headers)
        http_client.open()
        protocol_factory = TCompactProtocolAcceleratedFactory()
        provider = FServiceProvider(http_client, FProtocolFactory(protocol_factory))
        return provider


class TalkClient(Client, Talk):
    pass


class TalkClientFactory(ClientFactory):
    def create(self, path: str, headers: Dict) -> TalkClient:
        provider = self.get_provider(path, headers)
        return TalkClient(provider)


class AuthClient(Client, Auth):
    pass


class AuthClientFactory(ClientFactory):
    def create(self, path: str, headers: Dict) -> AuthClient:
        provider = self.get_provider(path, headers)
        return AuthClient(provider)
