"""
 Copyright (c) 2019 4masaka

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

from logging import getLogger
from typing import Optional, Tuple, Dict

# import requests
import aiohttp
from thrift.protocol.TCompactProtocol import TCompactProtocol
from thrift.transport.TTransport import TMemoryBuffer

from .config import Config, Endpoints
from .e2ee import decrypt_keychain, generate_asymmetric_keypair, create_secret_query
from .line_thrift.line import (
    E2EEKeyChain,
    IdentityProvider,
    LoginRequest,
    LoginResult,
    LoginResultType,
    LoginType,
)
from .auth import AuthApiFactory
from .talk import TalkApiFactory

logger = getLogger(__name__)

AuthInfo = Tuple[str, Dict]


class Client:
    """Clientクラス

    Attributes:
        config: Configオブジェクト
        endpoints: Endpointsオブジェクト
    """

    def __init__(
        self,
        custom_config: Optional[Config] = None,
        custom_endpoints: Optional[Endpoints] = None,
    ):
        self.config: Config = custom_config() if custom_config else Config()
        self.endpoints: Endpoints = custom_endpoints() if custom_endpoints else Endpoints()
        # self.loop = loop or asyncio.get_event_loop()

        self.host = self.config.host
        self.user_agent = self.config.user_agent
        self.line_app = self.config.line_app

        self.headers = {
            "X-Line-Application": self.line_app,
            "User-Agent": self.user_agent,
        }

    async def login_with_qrcode(self):
        qr_conn = TalkApiFactory(self.host).create(
            path=self.endpoints.registration, headers=self.headers
        )
        qr_verifier = await qr_conn.issue_qr_verifier(
            keep_logged_in=False, system_name=self.config.system_name
        )
        key_pair = generate_asymmetric_keypair()
        # query = generate_query(key_pair.public_key)
        secret_query = create_secret_query(key_pair.public_key)
        url = f"line://au/q/{qr_verifier}?secret={secret_query}&e2eeVersion=1"
        print(url)
        auth_verifier, metadata = await self.verify_auth(qr_verifier)
        encrypted_keychain = metadata["encryptedKeyChain"]
        _ = metadata["hashKeyChain"]
        public_key = metadata["publicKey"]
        keychain_data = decrypt_keychain(key_pair, encrypted_keychain, public_key)
        keychain = self.read_keychain(keychain_data)

        login_req = LoginRequest(
            type=LoginType.QRCODE,
            identityProvider=IdentityProvider.LINE,
            keepLoggedIn=False,
            accessLocation="127.0.0.1",
            verifier=auth_verifier,
            secret=key_pair.public_key,
            e2eeVersion=1,
        )
        login_result: LoginResult = (await self.login(login_req))
        self.headers["X-Line-Access"] = login_result.authToken

    async def verify_auth(self, qr_verifier: str) -> AuthInfo:
        self.headers["X-Line-Access"] = qr_verifier
        async with aiohttp.request(
            "GET",
            url=f"https://{self.host}{self.endpoints.auth_verify}",
            headers=self.headers,
            raise_for_status=True,
        ) as res:
            result = (await res.json())["result"]
            auth_verifier = result["verifier"]
            metadata = result["metadata"]

            return auth_verifier, metadata

    def read_keychain(self, keychain_data: bytes) -> E2EEKeyChain:
        keychain = E2EEKeyChain()
        buffer = TMemoryBuffer(keychain_data)
        protocol = TCompactProtocol(buffer)
        keychain.read(protocol)

        return keychain

    async def login(self, login_req: LoginRequest) -> str:
        login_conn = AuthApiFactory(self.host).create(
            self.endpoints.no_auth, self.headers
        )
        return (await login_conn.login(login_req))
