import logging

log = logging.getLogger(__name__)

from pyramid.request import Request
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import DENY_ALL
from pyramid.security import ALL_PERMISSIONS


class BaseView(object):
    __parent__ = None

    @property
    def __acl__(self):
        return [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, Authenticated, 'admin'),
        ]

    def __init__(self, request: Request):
        self.request = request
        self.view_name = type(self).__name__


    def __getitem__(self, key):
        raise KeyError


class SecureView(BaseView):
    __parent__ = BaseView.__name__

    @property
    def __acl__(self):
        return [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, Authenticated, 'admin'),
            DENY_ALL
        ]

    def __init__(self, request: Request):
        self.request = request
        self.view_name = type(self).__name__


# Imports:
from .errors import *
from .dnsapi import DnsApiViews
