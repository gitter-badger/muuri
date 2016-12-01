"""
Database errors
"""

import logging

log = logging.getLogger(__name__)

from pyramid.request import Request
from pyramid.view import view_config
from pyramid.i18n import TranslationString as _

# Connection error
from sqlalchemy.exc import InterfaceError as dberr_interface


@view_config(context=dberr_interface, renderer='templates/error_database.pt')
def dberror_interface_err(exc: dberr_interface, request: Request):
    msg = ""
    request.response.status = 500

    args = getattr(exc.orig, 'args', [])
    if len(args) > 0:
        errs = []
        for i in args:
            if isinstance(i, ConnectionRefusedError):
                errs.append(_(u"Connection was refused by database.") + " " + _(u"Check database settings."))
        if len(errs) > 0:
            msg = _(u"Error:") + " " + ", ".join(errs)

    return {'message': msg}


# Table missing, etc
from sqlalchemy.exc import ProgrammingError as dberr_programming


@view_config(context=dberr_programming, renderer='templates/error_database.pt')
def dberror_programming(exc: dberr_programming, request: Request):
    msg = ""
    request.response.status = 500

    args = getattr(exc.orig, 'args', None)
    if len(args) > 0:
        msg = _(u"Error code: {0} ({1}{2}{3}) {4}").format(args[1], '', args[0], '', args[2])

    return {'message': msg}


# Record not found from database
from sqlalchemy.orm.exc import NoResultFound as dberr_notfound


@view_config(context=dberr_notfound, renderer='templates/error_database.pt')
def dberror_not_found(exc: dberr_notfound, request: Request):
    request.response.status = 404
    msg = _(u"Record was not found from database")

    return {'message': msg}


# DB connection dropped / Pool error
from sqlalchemy.exc import UnboundExecutionError as dberr_unbound


def dberror_unbound_err(exc: dberr_unbound, request: Request):
    request.response.status = 500
    msg = _(u"Binding error")
    return {'message': msg}
