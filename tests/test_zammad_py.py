#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `zammad_py` package."""
from conftest import zammad_vcr


class TestAPI:

    @zammad_vcr.use_cassette('tests/fixtures/zammad_users.yml', record='once')
    def test_users(self, zammad_api):
        all_users = zammad_api.user.all()
        assert all_users[-1]['id'] == 3
        assert all_users[-1]['firstname'] == 'Joe'
