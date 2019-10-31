# Copyright (c) 2019 4masaka
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABCMeta, abstractmethod
from typing import Dict


class ServiceClient(metaclass=ABCMeta):
    pass


class ServiceClientFactory(metaclass=ABCMeta):
    def create(self, path: str, headers: Dict):
        pass

    @abstractmethod
    def get_transport(self):
        NotImplementedError()

    @abstractmethod
    def get_protocol(self):
        NotImplementedError()


class TalkClient(ServiceClient):
    pass


class TalkClientFactory(ServiceClientFactory):
    pass


class AuthClient(ServiceClient):
    pass


class AuthClientFactory(ServiceClientFactory):
    pass
