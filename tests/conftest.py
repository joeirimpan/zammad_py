# -*- coding: utf-8 -*-
import os
import vcr
import pytest

from zammad_py.api import ZammadAPI


zammad_vcr = vcr.VCR(
    filter_headers=[
        'Authorization',
    ]
)


@pytest.fixture
def zammad_api():
    return ZammadAPI(
        username=os.environ['ZAMMAD_USERNAME'],
        password=os.environ['ZAMMAD_PASSWORD'],
        host=os.environ['ZAMMAD_HOST'],
        is_secure=False
    )
