"""
Default layout(s)
"""

import logging

from pyramid.request import Request
from pyramid_layout.layout import layout_config

log = logging.getLogger(__name__)

from pyramid.config import Configurator


@layout_config(name='app', template='muuri:templates/default_layout.pt')
class AppLayout(object):
    def __init__(self, context, request: Request):
        pass


def includeme(config: Configurator):
    config.add_layout(AppLayout, 'muuri:views/templates/default_layout.pt')
