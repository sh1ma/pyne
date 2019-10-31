from types import TracebackType
from typing import Optional, Type, Dict
from thrift.transport.TTransport import TMemoryBuffer
from thrift.transport.TTransport import TTransportBase
from frugal.context import FContext
from frugal.aio.transport import FTransportBase
import aiohttp


class HttpClient(FTransportBase):
    def __init__(
        self,
        uri: str,
        headers: Optional[Dict] = None,
        request_capacity: int = 0,
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
    def get_client(self, scheme: str, host: str, path: str, port: int, headers: Dict):
        uri = f"{scheme}://{host}{path}:{port}"
        return HttpClient(uri, headers)
