"""
test_api.py
"""

# pylint: disable=redefined-outer-name, invalid-name

import pytest
from frugal.context import FContext

from pyne.talk import TalkApi, TalkApiFactory
from pyne.config import Config, Endpoints

pytestmark = pytest.mark.asyncio


@pytest.fixture
def api():
    """
    `TalkApi`を生成するフィクスチャ
    """
    config = Config()
    endpoints = Endpoints()
    return TalkApiFactory(config.host).create(
        endpoints.registration,
        headers={
            "X-Line-Application": config.line_app,
            "User-Agent": config.user_agent,
        }
    )


async def test_get_auth_qrcode(api: TalkApi):
    """`getAuthQrcode`のテストコード

    この関数で実際にAPIとの疎通が出来るか確認する
    """
    res = await api.getAuthQrcode(FContext(), False, "pyne", False)
    assert bool(res)
