#!/usr/bin/env python

"""Tests for `zammad_py` package."""
import io
import re

import pytest

from zammad_py.enums import KnowledgeBaseAnswerPublicity
from zammad_py.exceptions import (
    InvalidTypeError,
    MissingParameterError,
    UnusedResourceError,
)

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

    @pytest.mark.vcr()
    def test_knowledge_bases(self, zammad_api):
        structure = zammad_api.knowledge_bases.init()
        assert "KnowledgeBase" in structure
        assert "KnowledgeBaseLocale" in structure
        if structure["KnowledgeBase"]["1"]["category_ids"]:
            assert "KnowledgeBaseCategory" in structure

        settings = {
            "active": True,
            "homepage_layout": "grid",
            "color_highlight": "#38ae6a",
        }
        manage_response = zammad_api.knowledge_bases.manage(1, settings)
        assert manage_response["active"] is True
        assert manage_response["homepage_layout"] == "grid"

        permissions = zammad_api.knowledge_bases.show_permissions(1)
        assert "roles_reader" in permissions
        assert "roles_editor" in permissions

        new_permissions = {
            "permissions_dialog": {"permissions": {"1": "editor", "2": "reader"}}
        }
        change_permissions_response = zammad_api.knowledge_bases.change_permissions(
            1, new_permissions
        )
        assert "roles_reader" in change_permissions_response
        assert "roles_editor" in change_permissions_response

        reorder_sub_categories_params = {"ordered_ids": [3, 2]}
        reorder_sub_categories_response = (
            zammad_api.knowledge_bases.reorder_sub_categories(
                1, 1, reorder_sub_categories_params
            )
        )
        assert "KnowledgeBaseCategory" in reorder_sub_categories_response
        assert "KnowledgeBase" in reorder_sub_categories_response

        reorder_root_categories_params = {"ordered_ids": [5, 4, 1]}
        reorder_root_categories_response = (
            zammad_api.knowledge_bases.reorder_root_categories(
                1, reorder_root_categories_params
            )
        )
        assert "KnowledgeBaseCategory" in reorder_root_categories_response
        assert "KnowledgeBase" in reorder_root_categories_response

        kb = zammad_api.knowledge_bases

        unused_calls = [
            (kb.all, []),
            (kb.search, ["query"]),
            (kb.find, [1]),
            (kb.create, [{}]),
            (kb.update, [1, {}]),
            (kb.destroy, [1]),
        ]

        for method, args in unused_calls:
            with pytest.raises(UnusedResourceError) as excinfo:
                method(*args)
            assert "is not available for the KnowledgeBases resource" in str(
                excinfo.value
            )

    @pytest.mark.vcr()
    def test_knowledge_bases_answers(self, zammad_api):
        create_params = {
            "knowledge_base_id": 1,
            "category_id": 1,
            "title": "Initial Answer Title",
            "content": "This is the initial content.",
        }
        create_response = zammad_api.knowledge_bases_answers.create(create_params)
        assert "id" in create_response
        assert "assets" in create_response

        answer_id = create_response["id"]

        find_response = zammad_api.knowledge_bases_answers.find_answer(1, answer_id)
        assert find_response["id"] == answer_id
        assert "assets" in find_response

        update_params = {
            "answer_id": answer_id,
            "category_id": 1,
            "title": "Updated Answer Title",
        }
        update_response = zammad_api.knowledge_bases_answers.update(1, update_params)
        assert update_response["id"] == answer_id
        assert "assets" in update_response

        visibility_response = (
            zammad_api.knowledge_bases_answers.change_answer_visibility(
                1, answer_id, KnowledgeBaseAnswerPublicity.PUBLICLY
            )
        )
        assert "id" in visibility_response

        attachment_content = io.BytesIO(b"Hello Zammad")
        attachment_response = zammad_api.knowledge_bases_answers.add_attachment(
            1, answer_id, attachment_content
        )
        assert "id" in attachment_response or attachment_response is not None

        if "attachment_ids" in attachment_response:
            attachment_id = attachment_response["attachment_ids"][0]
            delete_attachment_res = (
                zammad_api.knowledge_bases_answers.delete_attachment(
                    1, answer_id, attachment_id
                )
            )
            assert delete_attachment_res is not None

        destroy_response = zammad_api.knowledge_bases_answers.destroy_answer(
            1, answer_id
        )
        assert destroy_response is not None

        kba = zammad_api.knowledge_bases_answers
        unused_calls = [
            (kba.all, []),
            (kba.search, ["query"]),
            (kba.find, [1]),
            (kba.destroy, [1]),
        ]

        for method, args in unused_calls:
            with pytest.raises(UnusedResourceError) as excinfo:
                method(*args)
            assert "is not available for the KnowledgeBasesAnswers resource" in str(
                excinfo.value
            )

        with pytest.raises(InvalidTypeError):
            zammad_api.knowledge_bases_answers.create(["not", "a", "dict"])

        with pytest.raises(MissingParameterError):
            zammad_api.knowledge_bases_answers.create({"title": "No KB ID"})

    @pytest.mark.vcr()
    def test_knowledge_bases_categories(self, zammad_api):
        create_params = {
            "knowledge_base_id": 1,
            "name": "Documentation Category",
            "description": "A category for API documentation",
            "parent_id": None,
            "category_icon": "f115",
        }
        create_response = zammad_api.knowledge_bases_categories.create(create_params)
        assert "id" in create_response
        assert create_response["category_icon"] == create_params["category_icon"]

        category_id = create_response["id"]

        find_response = zammad_api.knowledge_bases_categories.find_category(
            1, category_id
        )
        assert find_response["id"] == category_id

        update_params = {"category_id": category_id, "name": "Updated Category Name"}
        update_response = zammad_api.knowledge_bases_categories.update(1, update_params)
        assert update_response["id"] == category_id

        permissions = zammad_api.knowledge_bases_categories.show_permissions(
            1, category_id
        )
        assert "roles_reader" in permissions
        assert "roles_editor" in permissions

        new_permissions = {"permissions_dialog": {"permissions": {"1": "editor"}}}
        perm_response = zammad_api.knowledge_bases_categories.change_permissions(
            1, category_id, new_permissions
        )
        assert "roles_editor" in perm_response

        reorder_params = {"ordered_ids": [10, 1]}
        reorder_response = zammad_api.knowledge_bases_categories.reorder_answers(
            1, 1, reorder_params
        )
        assert reorder_response is not None

        destroy_response = zammad_api.knowledge_bases_categories.destroy_category(
            1, category_id
        )
        assert destroy_response is not None

        kbc = zammad_api.knowledge_bases_categories
        unused_calls = [
            (kbc.all, []),
            (kbc.search, ["query"]),
            (kbc.find, [1]),
            (kbc.destroy, [1]),
        ]

        for method, args in unused_calls:
            with pytest.raises(UnusedResourceError) as excinfo:
                method(*args)
            assert "is not available for the KnowledgeBasesCategories resource" in str(
                excinfo.value
            )

        with pytest.raises(InvalidTypeError):
            zammad_api.knowledge_bases_categories.create("not a dict")

        with pytest.raises(MissingParameterError):
            zammad_api.knowledge_bases_categories.create({"name": "No KB ID"})

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
