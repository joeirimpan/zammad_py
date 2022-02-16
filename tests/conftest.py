import os
import sys

testpath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testpath + "/../")

import pytest  # noqa
import vcr  # noqa

from zammad_py import ZammadAPI  # noqa

zammad_vcr = vcr.VCR(
    filter_headers=[
        "Authorization",
    ]
)


@pytest.fixture
def zammad_api():
    return ZammadAPI(
        url="http://localhost/api/v1/",
        username="test",
        password="test",
    )
