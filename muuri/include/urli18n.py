"""
Enable language in URL
"""

import logging

from pyramid.request import Request

log = logging.getLogger(__name__)

from pyramid.config import Configurator

from muuri import AppRootFactory


def add_localized_route(config, name, pattern, factory=AppRootFactory, pregenerator=None, **kw):
    orig_factory = factory

    def wrapper_factory(request: Request):
        lang = request.matchdict['lang']
        request.path_lang = lang
        request.locale_name = lang

        if orig_factory:
            return orig_factory(request)

    orig_pregenerator = pregenerator

    def wrapper_pregenerator(request: Request, elements, kw):
        if 'lang' not in kw:
            kw['lang'] = request.locale_name
        if orig_pregenerator:
            return orig_pregenerator(elements, kw)
        return elements, kw

    if pattern.startswith('/'):
        new_pattern = pattern[1:]
    else:
        new_pattern = pattern

    new_pattern = '/{lang}/' + new_pattern
    config.add_route(name, new_pattern, factory=wrapper_factory, pregenerator=wrapper_pregenerator, **kw)


def includeme(config: Configurator):
    config.add_directive('add_localized_route', add_localized_route)
