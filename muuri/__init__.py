import logging

log = logging.getLogger(__name__)

from pyramid.config import Configurator

from pyramid.events import NewRequest
from pyramid.events import subscriber

from pyramid.security import Deny

from pyramid.request import Request

from pyramid.traversal import DefaultRootFactory
from pyramid.traversal import ResourceTreeTraverser

from beaker.middleware import SessionMiddleware

from sqlalchemy import engine_from_config

from .database import DBSession


class AppRootFactory(object):
    __parent__ = None
    __name__ = "AppRootFactory"

    @property
    def __acl__(self):
        return [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, Authenticated, 'admin'),
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

from pyramid.viewderivers import DefaultViewMapper

class AppViewMapper(DefaultViewMapper):
    def __init__(self, **kw):
        self.attr = kw.get('attr')

    def map_class(self, view):
        ret = super().map_class(view)
        #log.debug("="*60)
        #log.debug("CLASS:")
        #log.debug(vars(view))
        #log.debug("="*60)
        return ret

    def map_nonclass(self, view):
        ret = super().map_nonclass(view)
        #log.debug("="*60)
        #log.debug("NON CLASS:")
        #log.debug(vars(view))
        #log.debug("="*60)
        return ret

def main(global_config, **settings):
    config = Configurator(settings = settings)
    config.set_default_permission(Deny)
    config.set_root_factory(AppRootFactory)
    config.set_view_mapper(AppViewMapper)

    config.add_translation_dirs('locale')

    # Includes
    config.include('pyramid_chameleon')
    config.include('pyramid_layout')
    config.include('pyramid_tm')
    config.include("pyramid_beaker") # Browser session

    # App includes
    config.include('include.urli18n')
    config.include('include.layouts')
    config.include('include.routes')
    config.include('include.security')

    engine = engine_from_config(settings, 'sqlalchemy.', implicit_returning = False)
    DBSession.configure(bind = engine)

    config.scan()

    # Start app
    app = config.make_wsgi_app()
    app = SessionMiddleware(app)

    return app
