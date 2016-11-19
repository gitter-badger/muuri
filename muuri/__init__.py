import logging

log = logging.getLogger(__name__)

from pyramid.request import Request

from pyramid.config import Configurator

from pyramid.events import NewRequest
from pyramid.events import subscriber

from beaker.middleware import SessionMiddleware

from sqlalchemy import engine_from_config

from .database import DBSession

@subscriber(NewRequest)
def ReqLanguage(event: NewRequest):
    """
    Read language code from URL and set it to request object
    """
    request = event.request.path
    if request.count("/") >= 2 and len(request) >= 4:
        lang = request[1:].split("/", 1)[0]
        if not lang.isalpha():
            import pyramid.httpexceptions as exc
            raise exc.HTTPInternalServerError("Invalid language")

        event.request.locale_name = lang


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.add_translation_dirs('locale')

    # Includes
    config.include('pyramid_chameleon')
    config.include('pyramid_layout')
    config.include('pyramid_tm')
    config.include("pyramid_beaker")
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
