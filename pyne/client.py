# Copyright (c) 2019 4masaka
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABCMeta, abstractmethod
from typing import Dict

from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
from frugal.provider import FServiceProvider
from frugal.protocol import FProtocolFactory

from http_client import HttpClientFactory


class ServiceClient(metaclass=ABCMeta):
    pass


class ServiceClientFactory(metaclass=ABCMeta):
    def __init__(self, host: str = "legy-jp-addr.line.naver.jp"):
        self.host = host

    @abstractmethod
    def create(self, path: str, headers: Dict):
        pass

    def get_provider(self, path, headers):
        http_client = HttpClientFactory(self.host).get_client(path, headers)
        http_client.open()
        protocol_factory = TCompactProtocolAcceleratedFactory()
        provider = FServiceProvider(http_client, FProtocolFactory(protocol_factory))
        return provider


class TalkClient(ServiceClient):
    pass


class TalkClientFactory(ServiceClientFactory):
    super.__init__()

    def create(self, path, headers):
        provider = self.get_provider(path, headers)
        service_client = TalkService.Client
        return service_client(provider)


class AuthClient(ServiceClient):
    pass


class AuthClientFactory(ServiceClientFactory):
    super.__init__()

    def create(self, path, headers):
        provider = self.get_provider(path, headers)
        service_client = AuthService.Client
        return service_client(provider)
