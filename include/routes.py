import logging

log = logging.getLogger(__name__)

from pyramid.security import NO_PERMISSION_REQUIRED

from pyramid.config import Configurator

def includeme(config: Configurator):
    config.add_static_view('static', 'muuri:static', cache_max_age = 10, permission = NO_PERMISSION_REQUIRED)

    # Default routes:
    config.add_localized_route('home', '/', permission = NO_PERMISSION_REQUIRED)
    config.add_localized_route('login', '/login', permission = NO_PERMISSION_REQUIRED)
    config.add_localized_route('logout', '/logout', permission = 'logged-in')

    # Modules:
    config.add_localized_route('dnsapi.home', '/dnsapi', permission = 'logged-in')
    config.add_localized_route('dnsapi.add', '/dnsapi/add', permission = 'logged-in')
    config.add_localized_route('dnsapi.zones', '/dnsapi/{id}/zones', permission = 'logged-in')
    config.add_localized_route('dnsapi.zone', '/dnsapi/{id}/zone/{zone}', permission = 'logged-in')

    config.add_route('test', '/test')