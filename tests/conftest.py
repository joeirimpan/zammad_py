import pytest
import vcr

from zammad_py import ZammadAPI

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
