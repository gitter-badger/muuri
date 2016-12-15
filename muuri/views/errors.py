"""
Default errors
"""

import logging

log = logging.getLogger(__name__)

from pyramid.request import Request

from pyramid.httpexceptions import HTTPInternalServerError

from pyramid.view import view_config
from pyramid.view import notfound_view_config
from pyramid.view import forbidden_view_config


@view_config(context=HTTPInternalServerError, renderer='templates/500.pt')
def error_internal(request: Request):
    """
    500
    """
    request.response.status = 500
    return {}


@notfound_view_config(renderer='templates/404.pt')
def error_notfound(request: Request):
    """
    404
    """
    if request.path == "/" or request.path.count('/') == 1:
        """
        Redirect to default language
        """
        from pyramid.threadlocal import get_current_registry
        deflang = get_current_registry().settings['pyramid.default_locale_name']
        redirect = "/" + deflang + "/"

        from pyramid.httpexceptions import HTTPFound
        return HTTPFound(location=redirect)

    request.response.status = 404
    return {}


@forbidden_view_config(renderer='templates/403.pt')
def error_forbidden(request: Request):
    """
    403
    """
    request.response.status = 403

    return {}
