# -*- coding: utf-8 -*-

"""Main module."""
import atexit
from contextlib import contextmanager

import requests
from requests.exceptions import HTTPError

from zammad_py.exceptions import ConfigException


__all__ = ['ZammadAPI']


class ZammadAPI(object):

    def __init__(
        self, host, username=None, password=None, http_token=None, oauth2_token=None,
        on_behalf_of=None, is_secure=True
    ):
        self.url = 'https://%s/api/v1/' % host
        if not is_secure:
            self.url = self.url.replace('https', 'http')
        self._username = username
        self._password = password
        self._http_token = http_token
        self._oauth2_token = oauth2_token
        self._on_behalf_of = on_behalf_of
        self._check_config()

        self.session = requests.Session()
        atexit.register(self.session.close)
        self.session.headers['User-Agent'] = 'Zammad API Python'
        if self._http_token:
            self.session.headers['Authorization'] = \
                'Token token=%s' % self._http_token
        elif oauth2_token:
            self.session.headers['Authorization'] = \
                'Bearer %s' % self._oauth2_token
        else:
            self.session.auth = (self._username, self._password)

        if self._on_behalf_of:
            self.session.headers['X-On-Behalf-Of'] = \
                self._on_behalf_of

    def _check_config(self):
        """Check the configuration
        """
        if not self.url:
            raise ConfigException('Missing url in config')
        if self._http_token:
            return
        if self._oauth2_token:
            return
        if not self._username:
            raise ConfigException('Missing username in config')
        if not self._password:
            raise ConfigException('Missing password in config')

    @property
    def on_behalf_of(self):
        return self._on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value):
        self._on_behalf_of = value
        self.session.headers['X-On-Behalf-Of'] = \
                self._on_behalf_of

    @contextmanager
    def request_on_behalf_of(self, on_behalf_of):
        self.session.headers['X-On-Behalf-Of'] = \
            on_behalf_of
        yield self
        self.session.headers['X-On-Behalf-Of'] = \
            self._on_behalf_of

    @property
    def group(self):
        """Return a `Group` instance
        """
        return Group(connection=self)

    @property
    def organization(self):
        """Return a `Organization` instance
        """
        return Organization(connection=self)

    @property
    def ticket(self):
        """Return a `Ticket` instance
        """
        return Ticket(connection=self)

    @property
    def ticket_article(self):
        """Return a `TicketArticle` instance
        """
        return TicketArticle(connection=self)

    @property
    def ticket_article_attachment(self):
        """Return a `TicketArticleAttachment` instance
        """
        return TicketArticleAttachment(connection=self)

    @property
    def ticket_priority(self):
        """Return a `TicketPriority` instance
        """
        return TicketPriority(connection=self)

    @property
    def ticket_state(self):
        """Return a `TicketState` instance
        """
        return TicketState(connection=self)

    @property
    def user(self):
        """Return a `User` instance
        """
        return User(connection=self)


class Pagination(object):

    def __init__(self, items, resource, filters=None, page=1):
        self._items = items
        self._page = page
        self._resource = resource
        self._filters = filters

    def __iter__(self):
        for item in self._items:
            yield item

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def next_page(self):
        self._page += 1
        return self._resource.all(
            page=self._page,
            filters=self._filters
        )

    def prev_page(self):
        self._page -= 1
        return self._resource.all(
            page=self._page,
            filters=self._filters
        )


class Resource(object):

    def __init__(self, connection, per_page=10):
        self._connection = connection
        self._per_page = per_page

    @property
    def url(self):
        """Returns a the full url concatenated with the resource class name
        """
        return self._connection.url + self.path_attribute

    @property
    def per_page(self):
        return self._per_page

    @per_page.setter
    def per_page(self, value):
        self._per_page = value

    def _raise_or_return_json(self, response):
        """Raise HTTPError before converting response to json

        :param response: Request response object
        """
        try:
            response.raise_for_status()
        except HTTPError:
            raise

        try:
            json_value = response.json()
        except ValueError:
            return response.content
        else:
            return json_value

    def all(self, page=1, filters=None):
        """Returns the list of resources

        :param page: Page number
        :param filters: Filter arguments like page, per_page
        """
        params = filters or {}
        params.update({
            'page': page,
            'per_page': self._per_page,
            'expand': 'true'
        })
        response = self._connection.session.get(self.url, params=params)
        data = self._raise_or_return_json(response)
        return Pagination(
            items=data,
            resource=self,
            filters=filters,
            page=page
        )

    def search(self, params):
        """Search using the given parameters

        :param params: Search parameters
        """
        response = self._connection.session.get(
            self.url + '/search',
            params=params
        )
        return self._raise_or_return_json(response)

    def find(self, id):
        """Return the resource associated with the id

        :param id: Resource id
        """
        response = self._connection.session.get(
            self.url + '/%s?expand=true' % id
        )
        return self._raise_or_return_json(response)

    def create(self, params):
        """Create the requested resource

        :param params: Resource data for creating
        """
        response = self._connection.session.post(
            self.url + '?expand=true',
            json=params
        )
        return self._raise_or_return_json(response)

    def update(self, id, params):
        """Update the requested resource

        :param id: Resource id
        :param params: Resource data for updating
        """
        response = self._connection.session.put(
            self.url + '/%s' % id,
            json=params
        )
        return self._raise_or_return_json(response)

    def destroy(self, id):
        """Delete the resource associated with the id

        :param id: Resource id
        """
        response = self._connection.session.delete(
            self.url + '/%s?expand=true' % id
        )
        return self._raise_or_return_json(response)


class Group(Resource):

    path_attribute = 'groups'


class Organization(Resource):

    path_attribute = 'organizations'


class Ticket(Resource):

    path_attribute = 'tickets'

    def articles(self, id):
        """Returns all the articles associated with the ticket id

        :param id: Ticket id
        """
        response = self._connection.session.get(
            self._connection.url +
            'ticket_articles/by_ticket/%s?expand=true' % id
        )
        return self._raise_or_return_json(response)


class TicketArticle(Resource):

    path_attribute = 'ticket_articles'


class TicketArticleAttachment(Resource):

    path_attribute = 'ticket_attachment'

    def download(self, id, article_id, ticket_id):
        """Download the ticket attachment associated with the ticket id

        :param id: Ticket attachment id
        :param article_id: Ticket article id
        :param ticket_id: Ticket id
        """
        response = self._connection.session.get(
            self.url + '/%s/%s/%s' % (ticket_id, article_id, id)
        )
        return self._raise_or_return_json(response)


class TicketPriority(Resource):

    path_attribute = 'ticket_priorities'


class TicketState(Resource):

    path_attribute = 'ticket_states'


class User(Resource):

    path_attribute = 'users'

    def me(self):
        """Returns current user information
        """
        response = self._connection.session.get(self.url + '/me')
        return self._raise_or_return_json(response)


class OnlineNotification(Resource):

    path_attribute = 'online_notifications'

    def mark_all_read(self):
        """Marks all online notification as read
        """
        response = self._connection.session.post(
            self.url + '/mark_all_as_read'
        )
        return self._raise_or_return_json(response)


class Object(Resource):

    path_attribute = 'object_manager_attributes'

    def execute_migrations(self):
        """Executes all database migrations
        """
        response = self._connection.session.post(
            self._connection.url +
            'object_manager_attributes_execute_migrations'
        )
        return self._raise_or_return_json(response)


class TagList(Resource):

    path_attribute = 'tag_list'
