import logging

log = logging.getLogger(__name__)

from pyramid.view import view_defaults
from pyramid.request import Request as Req


class BaseView(object):
    __parent__ = None
    request = None

    def __init__(self, request: Req):
        self.request = request
        self.view_name = type(self).__name__

    def __getitem__(self, key):
        raise KeyError


@view_defaults(permission='logged-in')
class SecureView(BaseView):
    __parent__ = None

    def __init__(self, request: Req):
        self.request = request
        self.view_name = type(self).__name__


# Imports:
from .errors import *
