"""
Default views
"""

import subprocess
import logging

from pyramid.request import Request
from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.view import view_config
from pyramid.view import notfound_view_config
from pyramid.view import forbidden_view_config
from pyramid.i18n import TranslationString as _
import pyramid_tm

from pyramid.security import remember
from pyramid.security import forget

log = logging.getLogger(__name__)


class BaseView(object):
    pass


from sqlalchemy.exc import ProgrammingError as dberr


@view_config(context = dberr, renderer = 'templates/error_database.pt')
def dberror(exc: dberr, request: Request):
    msg = ""
    request.response.status = 500

    args = getattr(exc.orig, 'args', None)
    if len(args) > 0:
        msg = _(u"Error code: {0} ({1}{2}{3}) {4}").format(args[1], '', args[0], '', args[2])

    return {'message': msg}


from sqlalchemy.orm.exc import NoResultFound as dberr_notfound


@view_config(context = dberr_notfound, renderer = 'templates/error_database.pt')
def dberror(exc: dberr_notfound, request: Request):
    msg = _(u"Record was not found from database")

    return {'message': msg}


@view_config(context = HTTPInternalServerError, renderer = 'templates/500.pt')
def internalerror(request: Request):
    request.response.status = 500
    return {}


@notfound_view_config(renderer = 'templates/404.pt')
def notfound(request: Request):
    if request.path == "/" or request.path.count('/') == 1:
        """
        Redirect to default language
        """
        import pyramid.httpexceptions as exc
        from pyramid.threadlocal import get_current_registry
        deflang = get_current_registry().settings['pyramid.default_locale_name']
        redirect = "/" + deflang + "/"
        return exc.HTTPFound(location = redirect)

    request.response.status = 404
    return {}


@forbidden_view_config(renderer = 'templates/403.pt')
def forbidden(request: Request):
    request.response.status = 403
    return {}


@view_config(route_name = 'home', renderer = 'templates/home.pt')
def my_view(request: Request):
    out = ""

    if request.authenticated_userid:
        with subprocess.Popen(["ip", "addr"], stdout = subprocess.PIPE) as proc:
            proc.wait(5)
            out = proc.stdout.read()

    return {'out': out}



"""
Login
"""
@view_config(route_name = 'login', renderer = 'templates/login.pt')
def app_login_view(request: Request):
    if request.authenticated_userid:
        # Already logged in -> redirect
        import pyramid.httpexceptions as exc
        return exc.HTTPFound(request.route_path('home'))

    user_not_found_error = {
        'page_background': 'warning',
        'page_title':      _(u"Login failed"),
        'page_text':       _(u"Check username and password."),
    }

    form_user = request.POST.get('user')
    form_password = request.POST.get('password')

    from ..models import UserModel, UserNotFoundException

    um = UserModel()

    if um.get_user_count() == 0:
        # No users in DB
        log.debug("Creating admin user")
        um.add_user(u"admin", u"admin")

    try:
        ses = um.create_session(form_user, form_password)
        request.session['userid'] = ses['userid']
        request.session.save()

        remember(request, ses['userid'])
        log.debug(ses)
        request.session['userid'] = ses['userid']
        request.session.save()
    except UserNotFoundException as exc:
        log.debug("User '%s' not found in database", form_user)
        return user_not_found_error
    except:
        raise

    # Redirect to front page
    import pyramid.httpexceptions as exc
    return exc.HTTPFound(request.route_path('home'))


@view_config(route_name = 'logout')
def app_logout_view(request: Request):
    if not request.authenticated_userid:
        import pyramid.httpexceptions as exc
        return exc.HTTPFound(request.route_path('home'))

    # Redirect to front page
    import pyramid.httpexceptions as exc
    return exc.HTTPFound(request.route_path('home'))
