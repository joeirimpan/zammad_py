import pytest

from zammad_py import ZammadAPI


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("Authorization", "user")],
    }


@pytest.fixture
def zammad_api():
    return ZammadAPI(
        url="http://localhost:8080/api/v1/",
        username="user",
        password="password",
    )
