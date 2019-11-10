"""
test_client.py
"""

# pylint: disable=redefined-outer-name, invalid-name

import pytest
from pyne.client import Client

pytestmark = pytest.mark.asyncio

@pytest.fixture
def client():
    client = Client(custom_config=None, custom_endpoints=None)
    return client


async def test_login_with_qr_code(client: Client):
    await client.login_with_qrcode()
