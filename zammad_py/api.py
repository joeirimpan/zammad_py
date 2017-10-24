# -*- coding: utf-8 -*-

"""Main module."""
import requests

from .extensions import ConfigException


class ZammadAPI(object):

    def __init__(
            self, username, password, host, http_token=None, oauth2_token=None
    ):
        self.url = 'http://%s/api/v1/' % host
        self._username = username
        self._password = password
        self._http_token = http_token
        self._oauth2_token = oauth2_token
        self.check_config()

        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Zammad API Python'
        if self._http_token:
            self.session.headers['Authorization'] = \
                'Token token=%s' % self._http_token
        elif oauth2_token:
            self.session.headers['Authorization'] = \
                'Bearer %s' % self._oauth2_token
        else:
            self.session.auth = (self._username, self._password)

    def check_config(self):
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

    def group(self):
        return Group(connection=self)

    def organization(self):
        return Organization(connection=self)

    def ticket(self):
        return Ticket(connection=self)

    def ticket_article(self):
        return TicketArticle(connection=self)

    def ticket_article_attachment(self):
        return TicketArticleAttachment(connection=self)

    def ticket_priority(self):
        return TicketPriority(connection=self)

    def ticket_state(self):
        return TicketState(connection=self)

    def user(self):
        return User(connection=self)


class Resource(object):

    def __init__(self, connection):
        self.connection = self.connection

    def all(self):
        pass

    def search(self):
        pass

    def find(self):
        pass

    def create(self):
        pass

    def destroy(self):
        pass

    def saved_attributes(self):
        pass

    def saved_new(self):
        pass

    def save_existing(self):
        pass

    def save_error(self):
        pass


class Group(Resource):

    path_attribute = 'groups'


class Organization(Resource):

    path_attribute = 'organizations'


class Ticket(Resource):

    path_attribute = 'tickets'

    def articles(self):
        pass

    def article(self):
        pass


class TicketArticle(Resource):

    path_attribute = 'ticket_articles'


class TicketArticleAttachment(Resource):

    path_attribute = 'ticket_attachment'

    def download(self):
        pass


class TicketPriority(Resource):

    path_attribute = 'ticket_priorities'


class TicketState(Resource):

    path_attribute = 'ticket_states'


class User(Resource):

    path_attribute = 'users'
