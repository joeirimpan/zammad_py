#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `zammad_py` package."""
from conftest import zammad_vcr


class TestAPI:

    @zammad_vcr.use_cassette(
        'tests/fixtures/zammad_users.yml', record_mode='new_episodes'
    )
    def test_users(self, zammad_api):
        all_users = zammad_api.user.all()
        assert all_users[-1]['id'] == 3
        assert all_users[-1]['firstname'] == 'Joe'

        current_user = zammad_api.user.me()
        assert current_user['id'] == 3
        assert current_user['firstname'] == 'Joe'

        current_user = zammad_api.user.find(3)
        assert current_user['id'] == 3
        assert current_user['firstname'] == 'Joe'

        new_user = zammad_api.user.create({
            'firstname': 'TestUser',
            'lastname': 'LastName'
        })
        assert new_user['id'] == 5
        assert new_user['firstname'] == 'TestUser'

        updated_user = zammad_api.user.update(5, {'firstname': 'TestUser1'})
        assert updated_user['firstname'] == 'TestUser1'

        deleted_user = zammad_api.user.destroy(5)
        assert deleted_user == dict()

        current_user, = zammad_api.user.search({'query': 'Joe'})
        assert current_user['id'] == 3
