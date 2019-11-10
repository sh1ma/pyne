"""
test_api.py
"""

# pylint: disable=redefined-outer-name, invalid-name

import pytest
from frugal.context import FContext

from pyne.client import Client

pytestmark = pytest.mark.asyncio


@pytest.fixture
def client():
    """
    Client
    """
    client = Client()
    return client


async def test_get_auth_qrcode(client: Client):
    """`getAuthQrcode`のテストコード

    この関数で実際にAPIとの疎通が出来るか確認する
    """
    res = await client.login_with_qrcode()
    print(client.headers)
