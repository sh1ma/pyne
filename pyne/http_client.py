# Copyright (c) 2019 4masaka
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from types import TracebackType
from typing import Dict, Optional, Type

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
        self.session = None

    def is_open(self) -> bool:
        if self.session is not None:
            return self.session.closed()
        return False

    async def open(self) -> None:
        self.session = aiohttp.ClientSession(
            headers=self.headers, raise_for_status=True
        )

    async def close(self) -> None:
        await self.session.close()

    async def oneway(self, context, payload):
        NotImplementedError()

    async def set_monitor(self, monitor):
        NotImplementedError()

    async def request(self, context: FContext, payload) -> TTransportBase:
        res = await self.session.post(self.uri, data=payload)
        return TMemoryBuffer(res.content.read())

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()


class HttpClientFactory:
    def __init__(self, host: str, port: int = 443, scheme: str = "https"):
        self.host = host
        self.port = port
        self.scheme = scheme

    def get_client(self, path: str, headers: Dict) -> HttpClient:
        uri = f"{self.scheme}://{self.host}{path}:{self.port}"
        return HttpClient(uri, headers)
