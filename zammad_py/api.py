"""Main module."""

import atexit
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Generator, List, Optional, Tuple

import requests
from requests.exceptions import HTTPError

from zammad_py.exceptions import ConfigException

__all__ = ["ZammadAPI"]


class ZammadAPI:
    def __init__(
        self,
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        http_token: Optional[str] = None,
        oauth2_token: Optional[str] = None,
        on_behalf_of: Optional[str] = None,
        additional_headers: Optional[List[Tuple[str, str]]] = None,
    ) -> None:
        self.url = url if url.endswith("/") else f"{url}/"
        self._username = username
        self._password = password
        self._http_token = http_token
        self._oauth2_token = oauth2_token
        self._on_behalf_of = on_behalf_of
        self._additional_headers = additional_headers
        self._check_config()

        self.session = requests.Session()
        atexit.register(self.session.close)
        self.session.headers["User-Agent"] = "Zammad API Python"
        if self._http_token:
            self.session.headers["Authorization"] = "Token token=%s" % self._http_token
        elif oauth2_token:
            self.session.headers["Authorization"] = "Bearer %s" % self._oauth2_token
        elif self._username and self._password:  # noqa: SIM106
            self.session.auth = (self._username, self._password)
        else:
            raise ValueError("Invalid Authentication information in config")

        if self._on_behalf_of:
            self.session.headers["X-On-Behalf-Of"] = self._on_behalf_of

        if self._additional_headers:
            for additional_header in self._additional_headers:
                self.session.headers[additional_header[0]] = additional_header[1]

    def _check_config(self) -> None:
        """Check the configuration"""
        if not self.url:
            raise ConfigException("Missing url in config")
        if self._http_token:
            return
        if self._oauth2_token:
            return
        if not self._username:
            raise ConfigException("Missing username in config")
        if not self._password:
            raise ConfigException("Missing password in config")

    @property
    def on_behalf_of(self) -> Optional[str]:
        return self._on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: str) -> None:
        self._on_behalf_of = value
        self.session.headers["X-On-Behalf-Of"] = self._on_behalf_of

    @contextmanager
    def request_on_behalf_of(
        self, on_behalf_of: str
    ) -> Generator["ZammadAPI", None, None]:
        """
        Use X-On-Behalf-Of Header, see https://docs.zammad.org/en/latest/api/intro.html?highlight=on%20behalf#actions-on-behalf-of-other-users

        :param on_behalf_of: The value of this header can be one of the following: user ID, login or email

        """
        initial_value = self.session.headers["X-On-Behalf-Of"]
        self.session.headers["X-On-Behalf-Of"] = on_behalf_of
        yield self
        self.session.headers["X-On-Behalf-Of"] = initial_value

    @property
    def group(self) -> "Group":
        """Return a `Group` instance"""
        return Group(connection=self)

    @property
    def organization(self) -> "Organization":
        """Return a `Organization` instance"""
        return Organization(connection=self)

    @property
    def role(self) -> "Role":
        """Return a `Role` instance"""
        return Role(connection=self)

    @property
    def ticket(self) -> "Ticket":
        """Return a `Ticket` instance"""
        return Ticket(connection=self)

    @property
    def link(self):
        """Return a `Link` instance"""
        return Link(connection=self)

    @property
    def ticket_article(self) -> "TicketArticle":
        """Return a `TicketArticle` instance"""
        return TicketArticle(connection=self)

    @property
    def ticket_article_attachment(self) -> "TicketArticleAttachment":
        """Return a `TicketArticleAttachment` instance"""
        return TicketArticleAttachment(connection=self)

    @property
    def ticket_article_plain(self) -> "TicketArticlePlain":
        """Return a `TicketArticlePlain` instance"""
        return TicketArticlePlain(connection=self)

    @property
    def ticket_priority(self) -> "TicketPriority":
        """Return a `TicketPriority` instance"""
        return TicketPriority(connection=self)

    @property
    def ticket_state(self) -> "TicketState":
        """Return a `TicketState` instance"""
        return TicketState(connection=self)

    @property
    def user(self) -> "User":
        """Return a `User` instance"""
        return User(connection=self)

    @property
    def taglist(self) -> "TagList":
        """Retrun a TagList instance"""
        return TagList(connection=self)

    @property
    def ticket_tag(self):
        """Return a `TicketTag` instance"""
        return TicketTag(connection=self)


class Pagination:
    def __init__(
        self,
        items,
        resource: "Resource",
        function_name: str,
        params=None,
        page: int = 1,
    ) -> None:
        self._items = items
        self._page = page
        self._resource = resource
        # Create a copy of params and remove page to prevent it from overriding the incremented page value
        self._params = params.copy() if params else {}
        if (
            self._params
            and "filters" in self._params
            and isinstance(self._params["filters"], dict)
            and "page" in self._params["filters"]
        ):
            self._params["filters"] = self._params["filters"].copy()
            self._params["filters"].pop("page", None)
        self._function_name = function_name

    def is_last_page(self) -> bool:
        """Check if the current page is the last page"""
        if len(self._items) < self._resource.per_page:
            return True
        return False

    def __iter__(self):
        yield from self._items

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int):
        return self._items[index]

    def __setitem__(self, index: int, value) -> None:
        self._items[index] = value

    def next_page(self) -> "Pagination":
        self._page += 1
        return getattr(self._resource, self._function_name)(
            page=self._page, **self._params
        )

    def prev_page(self) -> "Pagination":
        self._page -= 1
        return getattr(self._resource, self._function_name)(
            page=self._page, **self._params
        )


class Resource(ABC):
    def __init__(self, connection: ZammadAPI, per_page: int = 10) -> None:
        self._connection = connection
        self._per_page = per_page

    @property
    @abstractmethod
    def path_attribute(self) -> str:
        ...

    @property
    def url(self) -> str:
        """Returns a the full url concatenated with the resource class name"""
        return self._connection.url + self.path_attribute

    @property
    def per_page(self) -> int:
        return self._per_page

    @per_page.setter
    def per_page(self, value: int) -> None:
        self._per_page = value

    def _raise_or_return_json(self, response: requests.Response) -> Any:
        """Raise HTTPError before converting response to json

        :param response: Request response object
        """
        try:
            response.raise_for_status()
        except HTTPError:
            raise HTTPError(response.text)

        try:
            json_value = response.json()
        except ValueError:
            return response.content
        else:
            return json_value

    def all(self, page: int = 1, filters=None) -> Pagination:
        """Returns the list of resources

        :param page: Page number
        :param filters: Filter arguments including page, per_page if needed
        """
        params = filters.copy() if filters else {}

        # Set defaults only if not specified in filters
        if "page" not in params:
            params["page"] = page
        if "per_page" not in params:
            params["per_page"] = self._per_page
        if "expand" not in params:
            params["expand"] = "true"

        if "per_page" in params:
            self._per_page = params["per_page"]

        response = self._connection.session.get(self.url, params=params)
        data = self._raise_or_return_json(response)

        return Pagination(
            items=data,
            resource=self,
            function_name="all",
            params={"filters": params},
            page=params["page"],
        )

    def search(self, search_string: str, page: int = 1, filters=None) -> Pagination:
        """Returns the list of resources

        :param search_string: option to filter for
        :param page: Page number
        :param filters: Filter arguments like page, per_page
        """
        params = filters.copy() if filters else {}
        params.update({"query": search_string})

        # Set defaults only if not specified in filters
        if "page" not in params:
            params["page"] = page
        if "per_page" not in params:
            params["per_page"] = self._per_page
        if "expand" not in params:
            params["expand"] = "true"

        if "per_page" in params:
            self._per_page = params["per_page"]

        response = self._connection.session.get(self.url + "/search", params=params)
        data = self._raise_or_return_json(response)

        return Pagination(
            items=data,
            resource=self,
            function_name="search",
            params={"search_string": search_string, "filters": params},
            page=params["page"],
        )

    def find(self, id):
        """Return the resource associated with the id

        :param id: Resource id
        """
        response = self._connection.session.get(self.url + "/%s" % id)
        return self._raise_or_return_json(response)

    def create(self, params):
        """Create the requested resource

        :param params: Resource data for creating
        """
        response = self._connection.session.post(self.url, json=params)
        return self._raise_or_return_json(response)

    def update(self, id, params):
        """Update the requested resource

        :param id: Resource id
        :param params: Resource data for updating
        """
        response = self._connection.session.put(self.url + "/%s" % id, json=params)
        return self._raise_or_return_json(response)

    def destroy(self, id):
        """Delete the resource associated with the id

        :param id: Resource id
        """
        response = self._connection.session.delete(self.url + "/%s" % id)
        return self._raise_or_return_json(response)


class Group(Resource):
    path_attribute = "groups"


class Role(Resource):
    path_attribute = "roles"


class Organization(Resource):
    path_attribute = "organizations"


class Ticket(Resource):
    path_attribute = "tickets"

    def articles(self, id):
        """Returns all the articles associated with the ticket id

        :param id: Ticket id
        """
        response = self._connection.session.get(
            self._connection.url + "ticket_articles/by_ticket/%s?expand=true" % id
        )
        return self._raise_or_return_json(response)

    def tags(self, id):
        """Returns all the tags associated with the ticket id

        :param id: Ticket id
        """
        response = self._connection.session.get(
            self._connection.url + f"tags?object=Ticket&o_id={id}"
        )
        return self._raise_or_return_json(response)

    def merge(self, id, number):
        """Merges two tickets, (undocumented in Zammad Docs)
        If the objects are already merged, it will return "Object already exists!"
        Attention: Must use password to authenticate to Zammad, otherwise this will not work!
        :param id: Ticket id of the child
        :param number: Ticket Number of the Parent
        """

        response = self._connection.session.put(
            self._connection.url + f"ticket_merge/{id}/{number}"
        )
        return self._raise_or_return_json(response)


class Link(Resource):
    path_attribute = "links"

    def add(
        self,
        link_object_target_value,
        link_object_source_number,
        link_type="normal",
        link_object_target="Ticket",
        link_object_source="Ticket",
    ):
        """Create the link

        :params link_type: Link type ('normal', 'parent', 'child')
        :params link_object_target: (for now*: 'Ticket')
        :params link_object_target_value: Ticket ID
        :params link_object_source: (for now*: 'Ticket')
        :params link_object_source_number: Ticket Number (Not the ID!)

        *Currently, only Tickets can be linked together.
        """
        params = {
            "link_type": link_type,
            "link_object_target": link_object_target,
            "link_object_target_value": link_object_target_value,
            "link_object_source": link_object_source,
            "link_object_source_number": link_object_source_number,
        }

        response = self._connection.session.post(self.url + "/add", json=params)
        return self._raise_or_return_json(response)

    def remove(
        self,
        link_object_target_value,
        link_object_source_number,
        link_type="normal",
        link_object_target="Ticket",
        link_object_source="Ticket",
    ):
        """Remove the Link

        :params link_type: Link type ('normal', 'parent', 'child')
        :params link_object_target: (for now: 'Ticket')
        :params link_object_target_value: Ticket ID
        :params link_object_source: (for now: 'Ticket')
        :params link_object_source_number: Ticket ID
        """
        params = {
            "link_type": link_type,
            "link_object_target": link_object_target,
            "link_object_target_value": link_object_target_value,
            "link_object_source": link_object_source,
            "link_object_source_number": link_object_source_number,
        }

        response = self._connection.session.delete(self.url + "/remove", json=params)
        return self._raise_or_return_json(response)

    def get(self, id):
        """Returns all the links associated with the ticket id

        :param id: Ticket id
        """
        params = {"link_object": "Ticket", "link_object_value": id}
        response = self._connection.session.get(
            self._connection.url + self.path_attribute, params=params
        )
        return self._raise_or_return_json(response)


class TicketArticle(Resource):
    path_attribute = "ticket_articles"


class TicketArticleAttachment(Resource):
    path_attribute = "ticket_attachment"

    def download(self, id, article_id, ticket_id):
        """Download the ticket attachment associated with the ticket id

        :param id: Ticket attachment id
        :param article_id: Ticket article id
        :param ticket_id: Ticket id
        """
        response = self._connection.session.get(
            self.url + f"/{ticket_id}/{article_id}/{id}"
        )
        return self._raise_or_return_json(response)


class TicketArticlePlain(Resource):
    path_attribute = "ticket_article_plain"


class TicketPriority(Resource):
    path_attribute = "ticket_priorities"


class TicketState(Resource):
    path_attribute = "ticket_states"


class User(Resource):
    path_attribute = "users"

    def me(self):
        """Returns current user information"""
        response = self._connection.session.get(self.url + "/me")
        return self._raise_or_return_json(response)


class OnlineNotification(Resource):
    path_attribute = "online_notifications"

    def mark_all_read(self):
        """Marks all online notification as read"""
        response = self._connection.session.post(self.url + "/mark_all_as_read")
        return self._raise_or_return_json(response)


class Object(Resource):
    path_attribute = "object_manager_attributes"

    def execute_migrations(self):
        """Executes all database migrations"""
        response = self._connection.session.post(
            self._connection.url + "object_manager_attributes_execute_migrations"
        )
        return self._raise_or_return_json(response)


class TagList(Resource):
    """TagList handles tags in admin scope"""

    path_attribute = "tag_list"


class TicketTag(Resource):
    """handles tags in the ticket scope"""

    path_attribute = "tags"

    def add(self, id, tag, object="Ticket"):
        """Add a tag to a ticket

        :param id: Ticket id
        :param tag: Tag name
        :param object: Object to tag ((for now: 'Ticket'))
        """

        params = {
            "o_id": id,
            "item": tag,
            "object": object,
        }

        response = self._connection.session.post(self.url + "/add", json=params)
        return self._raise_or_return_json(response)

    def remove(self, id, tag, object="Ticket"):
        """Remove a tag from a ticket.

        :param id: Ticket id
        :param tag: Tag name
        :param object: Object to tag ((for now: 'Ticket'))
        """

        params = {
            "o_id": id,
            "item": tag,
            "object": object,
        }

        response = self._connection.session.delete(self.url + "/remove", json=params)
        return self._raise_or_return_json(response)
