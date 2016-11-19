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

from beaker.session import Session as beakersession

from pyramid.security import remember
from pyramid.security import forget

from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.security import Deny
from pyramid.security import Authenticated
from pyramid.security import DENY_ALL
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import NO_PERMISSION_REQUIRED


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
@view_config(route_name = 'login', renderer = 'templates/login.pt', permission = NO_PERMISSION_REQUIRED)
def app_login_view(request: Request):
    import pyramid.httpexceptions as exc

    if request.authenticated_userid:
        # Already logged in -> redirect
        return exc.HTTPFound(request.route_path('home'), comment = "Logged in user tried to log in")

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

    if form_user is None:
        form_user = ""

    if form_password is None:
        form_password = ""

    if form_user == "" and form_password == "":
        return {
            'page_background': 'warning',
            'page_title':      _(u"Login failed"),
            'page_text':       _(u"Fields were empty."),
        }

    if form_password == "":
        return {
            'page_background': 'warning',
            'page_title':      _(u"Login failed"),
            'page_text':       _(u"Password was empty."),
        }

    if form_user == "":
        return {
            'page_background': 'warning',
            'page_title':      _(u"Login failed"),
            'page_text':       _(u"User was empty."),
        }

    try:
        ses = um.create_session(form_user, form_password)
        from ..models import LoginLogModel
        lm = LoginLogModel()
        lm.add_log(ses['userid'])
        return exc.HTTPFound(location = request.route_path('home'), headers = remember(request, ses['userid']), comment = "Login")
    except UserNotFoundException as exc:
        log.debug("User '%s' not found in database", form_user)
        return user_not_found_error
    except:
        raise

    # Redirect to front page
    return exc.HTTPFound(request.route_path('home'))


@view_config(route_name = 'logout', permission = Authenticated)
def app_logout_view(request: Request):
    if not request.authenticated_userid:
        import pyramid.httpexceptions as exc
        return exc.HTTPFound(request.route_path('home'), comment = "Logged out user tried to logout")

    # Redirect to front page
    import pyramid.httpexceptions as exc
    return exc.HTTPFound(request.route_path('home'), forget(request))

@view_config(route_name = 'session_id_validate', permission = 'admin')
def validate_sesid(request: Request):
    beakersession.id