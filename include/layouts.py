"""
Default layout(s)
"""

from pyramid_layout.layout import layout_config
from pyramid.request import Request

import logging

log = logging.getLogger(__name__)


@layout_config(name='chameleon', template='muuri:templates/default_layout.pt')
class AppLayout(object):
    def __init__(self, context, request: Request):
        pass


def includeme(config):
    """
    Load
    """
    config.add_layout(AppLayout, 'muuri:views/templates/default_layout.pt')
    log.debug("included %s", __name__)
