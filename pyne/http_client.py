"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from typing import Dict, Optional

import aiohttp
from frugal.aio.transport import FTransportBase
from frugal.context import FContext
from thrift.transport.TTransport import TMemoryBuffer, TTransportBase


class HttpClient(FTransportBase):
    def __init__(
        self, uri: str, headers: Optional[Dict] = None, request_capacity: int = 0
    ) -> None:
        super().__init__(request_capacity)
        self.uri = uri
        self.headers = {
            "Content-Type": "application/x-thrift",
            "Accept": "application/x-thrift",
        }
        self.headers.update(headers)

    def is_open(self) -> bool:
        return True

    def open(self) -> None:
        return True

    async def close(self) -> None:
        NotImplementedError()

    async def oneway(self, context, payload):
        NotImplementedError()

    async def set_monitor(self, monitor):
        NotImplementedError()

    async def request(self, context: FContext, payload) -> TTransportBase:
        payload = payload[4:]
        async with aiohttp.request(
            "POST",
            url=self.uri,
            data=payload,
            headers=self.headers
        ) as res:
            return TMemoryBuffer(await res.content.read())

class HttpClientFactory:
    def __init__(self, host: str, port: int = 443, scheme: str = "https"):
        self.host = host
        self.port = port
        self.scheme = scheme

    def get_client(self, path: str, headers: Optional[Dict] = None) -> HttpClient:
        uri = f"{self.scheme}://{self.host}:{self.port}{path}"
        return HttpClient(uri, headers=headers)
