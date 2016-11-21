import logging

log = logging.getLogger(__name__)

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.security import Authenticated

from pyramid.config import Configurator

def includeme(config: Configurator):
    config.add_static_view('static', 'muuri:static', cache_max_age = 10, permission = NO_PERMISSION_REQUIRED)

    config.add_localized_route('home', '/', permission = NO_PERMISSION_REQUIRED)
    config.add_localized_route('login', '/login', permission = NO_PERMISSION_REQUIRED)
    config.add_localized_route('logout', '/logout', permission = 'admin')

    config.add_localized_route('session_id_validate', '/validate/{id}', permission = 'admin')

    config.add_localized_route('dnsapi.home', '/dnsapi', permission = 'admin')
    config.add_localized_route('dnsapi.add', '/dnsapi/add', permission = 'admin')
