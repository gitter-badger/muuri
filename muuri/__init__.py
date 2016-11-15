import logging

log = logging.getLogger(__name__)

from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy

from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from .database import Base
from .database import DBSession

@subscriber(NewRequest)
def ReqLanguage(event: NewRequest):
    """
    Read language code from URL and set it to request object
    """
    request = event.request.path
    if request.count("/") >= 2 and len(request) >= 4:
        event.request.locale_name = request[1:].split("/", 1)[0]


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('pyramid_chameleon')
    config.include('pyramid_layout')
    config.include('pyramid_tm')
    config.include("pyramid_beaker")

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    authn_policy = AuthTktAuthenticationPolicy(debug = True, secret = 'verysecret', hashalg = 'sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=1)

    config.add_translation_dirs('locale')

    config.include('include.urli18n')
    config.include('include.layouts')

    config.add_localized_route('home', '/')
    config.add_localized_route('login', '/login')
    config.add_localized_route('logout', '/logout')

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind = engine)

    config.scan()

    return config.make_wsgi_app()
