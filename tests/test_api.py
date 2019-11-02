"""
test_api.py
"""

# pylint: disable=redefined-outer-name, invalid-name

import pytest
from frugal.context import FContext

from pyne.api import TalkApi, TalkApiFactory

pytestmark = pytest.mark.asyncio


@pytest.fixture
def api():
    """
    `TalkApi`を生成するフィクスチャ
    """
    return TalkApiFactory("legy-jp-addr.line.naver.jp").create(
        "/api/v4/TalkService.do",
        headers={
            "X-Line-Application": "CHROMEOS\t2.2.2\tChrome_OS\t1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        },
    )


async def test_get_auth_qrcode(api: TalkApi):
    """`getAuthQrcode`のテストコード

    この関数で実際にAPIとの疎通が出来るか確認する
    """
    res = await api.getAuthQrcode(FContext(), False, "Sh1ma", False)
    assert bool(res) is True
