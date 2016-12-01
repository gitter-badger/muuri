import logging

log = logging.getLogger(__name__)

from pyramid.config import Configurator

from pyramid.events import NewRequest
from pyramid.events import subscriber

from pyramid.security import Deny
from pyramid.security import Allow
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Authenticated

from pyramid.request import Request

from beaker.middleware import SessionMiddleware

from sqlalchemy import engine_from_config

from .database import DBSession


class AppRootFactory:
    __parent__ = None

    @property
    def __acl__(self):
        return [
            (Allow, 'logged-in', ALL_PERMISSIONS),
            (Allow, Authenticated, ALL_PERMISSIONS),
        ]

    def __init__(self, request: Request):
        self.request = request


@subscriber(NewRequest)
def ReqLanguage(event: NewRequest):
    """
    Read language code from URL and set it to request object
    """
    lang = None
    request = event.request.path
    if request.count("/") >= 2 and len(request) >= 4:
        lang = request[1:].split("/", 1)[0]
        if not lang.isalpha():
            import pyramid.httpexceptions as exc
            raise exc.HTTPInternalServerError("Invalid language")

    event.request.locale_name = lang


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.set_root_factory(AppRootFactory)
    config.set_default_permission(Deny)

    config.add_translation_dirs('locale')

    # Includes
    config.include('pyramid_chameleon')
    config.include('pyramid_layout')
    config.include('pyramid_tm')
    config.include("pyramid_beaker")  # Browser session

    # App includes
    config.include('muuri.include.urli18n')
    config.include('muuri.include.layouts')
    config.include('muuri.include.routes')
    config.include('muuri.include.security')

    engine = engine_from_config(settings, 'sqlalchemy.', implicit_returning=False)
    DBSession.configure(bind=engine)

    config.scan()

    # Start app
    app = config.make_wsgi_app()
    app = SessionMiddleware(app)

    return app
