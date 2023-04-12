"""Module to handle Object instances"""
import atexit
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Generator, List, Optional, Tuple
from datetime import datetime
import requests
from requests.exceptions import HTTPError
from .api import ZammadAPI
from zammad_py.exceptions import ConfigException

__all__ = ["ZammadUser"]

class ZammadUser:
    NOEXPORT = [
        'NOEXPORT',
        'apiclient',
        'role_ids',
        'organization_id',
        'organization_ids',
        'authorization_ids',
        'karma_user_ids',
        'group_ids',
        'attr_dict',
        'changed_attributes'
    ]
    def __init__(
        self,
        apiclient: [ZammadAPI],
        login: [str] = None,
        firstname: [str] = None,
        lastname: [str] = None,
        email: [str] = None,
        attr_dict: [dict] = None,
                 ) -> None:
            self.changed_attributes = set()
            # TODO: Add clear-text attributes like "organization" or "roles" that show returns as organization_id or role_ids
            if apiclient is not None:
                self.apiclient = apiclient

                if attr_dict is not None:
                    for key, value in attr_dict.items():
                        setattr(self, key, value)
                elif login is None or firstname is None or lastname is None or email is None:
                    raise ValueError("if you don't provide attr_dict, you must provide: login, firstname, lastname and email")
                else:
                    self.login = login
                    self.firstname = firstname
                    self.lastname = lastname
                    self.email = email
            else:
                raise ValueError("apiclient must be provided")


    def __setattr__(self, name, value):
        if hasattr(self, name) and getattr(self, name) != value:
            self.changed_attributes.add(name)
        super().__setattr__(name, value)


    def _to_dict(self):
        attributes = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        allowed_attributes = [attr for attr in attributes if attr not in self.NOEXPORT]
        return {attr: getattr(self, attr) for attr in allowed_attributes}


    def _get_changed_attributes(self):
        changed_dict = {}
        for attr in self.changed_attributes:
            if attr not in self.NOEXPORT:
                changed_dict[attr] = getattr(self, attr)
        self.changed_attributes.clear()
        return changed_dict


    def create(self):
        # TODO: plaintext fields to create
        print(self._to_dict())
        created_dict = self.apiclient.user.create(params=self._to_dict())
        print(created_dict)
        for key, value in created_dict.items():
            setattr(self, key, value)


    def update(self):
        updated_dict = self.apiclient.user.update(self.id, params=self._get_changed_attributes())
        for key, value in updated_dict.items():
            setattr(self, key, value)


    def delete(self):
        self.apiclient.user.destroy(self.id)
