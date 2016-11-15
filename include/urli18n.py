"""
Enable language in URL
"""

from pyramid.request import Request

import logging

log = logging.getLogger(__name__)


def add_localized_route(config, name, pattern, factory=None, pregenerator=None, **kw):
    log.debug("called: %s", __name__)

    """Create path language aware routing paths.
    Each route will have /{lang}/ prefix added to them.
    Optionally, if default language is set, we'll create redirect from an URL without language path component to the URL with the language path component.
    """
    orig_factory = factory

    def wrapper_factory(request: Request):
        lang = request.matchdict['lang']
        # determine if this is a supported lang and convert it to a locale,
        # likely defaulting to your default language if the requested one is
        # not supported by your app
        request.path_lang = lang
        request.locale_name = lang

        if orig_factory:
            return orig_factory(request)

    orig_pregenerator = pregenerator

    def wrapper_pregenerator(request: Request, elements, kw):
        if 'lang' not in kw:
            # not quite right but figure out how to convert request._LOCALE_ back into a language url
            kw['lang'] = request.locale_name
        if orig_pregenerator:
            return orig_pregenerator(elements, kw)
        return elements, kw

    if pattern.startswith('/'):
        new_pattern = pattern[1:]
    else:
        new_pattern = pattern

    new_pattern = '/{lang}/' + new_pattern

    # Language-aware URL routed
    config.add_route(name, new_pattern, factory=wrapper_factory, pregenerator=wrapper_pregenerator, **kw)


def includeme(config):
    """
    Load
    """
    config.add_directive('add_localized_route', add_localized_route)
    log.debug("included %s", __name__)
