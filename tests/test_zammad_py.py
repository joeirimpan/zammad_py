#!/usr/bin/env python

"""Tests for `zammad_py` package."""
import re

import pytest

# from conftest import zammad_vcr


class TestAPI:
    @pytest.mark.vcr()
    def test_users(self, zammad_api):
        all_users = zammad_api.user.all()._items
        assert all_users[2]["id"] == 3
        assert all_users[2]["firstname"] == "John"

        current_user = zammad_api.user.me()
        assert current_user["id"] == 3
        assert current_user["firstname"] == "John"

        current_user = zammad_api.user.find(3)
        assert current_user["id"] == 3
        assert current_user["firstname"] == "John"

        new_user = zammad_api.user.create(
            {"firstname": "TestUser", "lastname": "LastName"}
        )
        assert new_user["firstname"] == "TestUser"

        updated_user = zammad_api.user.update(
            new_user["id"], {"firstname": "TestUser1"}
        )
        assert updated_user["firstname"] == "TestUser1"

        (current_user,) = zammad_api.user.search("John")
        assert current_user["id"] == 3

    @pytest.mark.vcr()
    def test_tickets(self, zammad_api):
        all_tickets = zammad_api.ticket.all()._items
        assert all_tickets[0]["id"] == 1
        assert all_tickets[0]["title"] == "Welcome to Zammad!"

        current_ticket = zammad_api.ticket.find(1)
        assert current_ticket["id"] == 1
        assert current_ticket["title"] == "Welcome to Zammad!"

        new_ticket = zammad_api.ticket.create(
            {
                "title": "some new title",
                "state": "new",
                "priority": "2 normal",
                "owner": "-",
                "customer": "nicole.braun@zammad.org",
                "group": "Users",
                "article": {
                    "sender": "Customer",
                    "type": "note",
                    "subject": "some subject",
                    "content_type": "text/plain",
                    "body": "some body\nnext line",
                },
            }
        )
        assert new_ticket["title"] == "some new title"
        assert new_ticket["customer_id"] == 2

        updated_ticket = zammad_api.ticket.update(
            new_ticket["id"], {"title": "TestTicket1"}
        )
        assert updated_ticket["title"] == "TestTicket1"

        deleted_ticket = zammad_api.ticket.destroy(new_ticket["id"])
        assert deleted_ticket == b""

        result = zammad_api.ticket.search("Welcome")._items
        assert result[0]["title"] == "Welcome to Zammad!"

    @pytest.mark.vcr()
    def test_groups(self, zammad_api):
        all_groups = zammad_api.group.all()._items
        assert all_groups[0]["id"] == 1
        assert all_groups[0]["note"] == "Standard Group/Pool for Tickets."

        current_group = zammad_api.group.find(1)
        assert current_group["id"] == 1
        assert current_group["note"] == "Standard Group/Pool for Tickets."

        new_group = zammad_api.group.create({"name": "Test1", "note": "note1"})
        assert new_group["name"] == "Test1"
        assert new_group["note"] == "note1"

        updated_group = zammad_api.group.update(new_group["id"], {"name": "Test2"})
        assert updated_group["name"] == "Test2"

        deleted_group = zammad_api.group.destroy(new_group["id"])
        assert deleted_group == {}

    @pytest.mark.vcr()
    def test_pagination(self, zammad_api):
        # Let us create 5 users
        users = []
        for index in range(5):
            users.append(
                zammad_api.user.create({"email": "pytest%s@example.com" % index})
            )
        paginated_response = zammad_api.user.all(filters={"per_page": 2})

        # assert there are 5 users emails
        data = []
        while True:
            for item in paginated_response:
                print(item)
                if re.match(r"pytest\d+@example\.com", item["email"]):
                    data.append(item["email"])
                assert item is not None
            print("last page?", paginated_response.is_last_page())
            if paginated_response.is_last_page():
                break
            paginated_response = paginated_response.next_page()

        assert len(data) == 5

        # Go to prev page
        prev_page = paginated_response.prev_page()
        for item in prev_page:
            assert item is not None
        for item in paginated_response:
            assert item is not None
        # Delete users
        for user in users:
            zammad_api.user.destroy(user["id"])

    def test_push_on_behalf_of_header(self, zammad_api):
        zammad_api.on_behalf_of = "USERX"
        with zammad_api.request_on_behalf_of("USERXX") as api:
            assert api.session.headers["X-On-Behalf-Of"] == "USERXX"

        assert api.session.headers.get("X-On-Behalf-Of") == "USERX"

    def test_trailing_slash_url(self):
        from zammad_py import ZammadAPI

        url = "https://zammad.example.com"

        z1 = ZammadAPI(url=url + "/", username="test", password="test")
        assert z1.url == f"{url}/"

        z2 = ZammadAPI(url=url, username="test", password="test")
        assert z2.url == f"{url}/"
