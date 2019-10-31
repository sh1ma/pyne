# Copyright (c) 2019 4masaka
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import asyncio

from .config import Config, Endpoints
from .api import AuthApiFactory, TalkApiFactory


class Client:
    """Clientクラス

    Attributes:
        config: Configオブジェクト
        endpoints: Endpointsオブジェクト
    """

    def __init__(self, custom_config: Config, custom_endpoints: Endpoints, loop=None):
        self.config = custom_config() if custom_config else Config()
        self.endpoints = custom_endpoints() if custom_endpoints else Endpoints()
        # self.loop = asyncio.get_event_loop() or None
