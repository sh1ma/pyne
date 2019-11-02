"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

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
        self.config: Config = custom_config() if custom_config else Config()
        self.endpoints: Endpoints = custom_endpoints() if custom_endpoints else Endpoints()
        # self.loop = loop or asyncio.get_event_loop()

        self.host = self.config.host
        self.user_agent = self.config.user_agent
        self.line_app = self.config.line_app

        self.headers = {
            "X-Line-Application": self.line_app,
            "User-Agent": self.line_app
        }
