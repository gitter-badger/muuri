import logging

log = logging.getLogger(__name__)

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age = 1)

    config.add_localized_route('home', '/')
    config.add_localized_route('login', '/login')
    config.add_localized_route('logout', '/logout')
    config.add_localized_route('session_id_validate', '/validate/{id}')
    config.add_localized_route('dnsapi.home', '/dnsapi')
    config.add_localized_route('dnsapi.add', '/dnsapi/add')

    log.debug("Routes loaded")