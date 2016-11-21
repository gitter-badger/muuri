"""
Default views
"""

import logging

log = logging.getLogger(__name__)

import subprocess

from pyramid.request import Request

from pyramid.view import view_config
from pyramid.view import view_defaults

from pyramid.i18n import TranslationString as _

from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.security import ALL_PERMISSIONS

from beaker.session import Session as beakersession

from . import BaseView

import pyramid.httpexceptions as httpexs

@view_config(route_name = 'session_id_validate', permission = 'admin')
def validate_sesid(request: Request):
    beakersession.id


@view_defaults(permission = NO_PERMISSION_REQUIRED)
class DefaultViews(BaseView):
    __parent__ = BaseView.__name__

    @property
    def __acl__(self):
        return [
            (Allow, 'admin', ALL_PERMISSIONS),
            (Allow, Authenticated, 'admin'),
        ]


    def __init__(self, request: Request):
        self.request = request
        self.view_name = type(self).__name__

    @view_config(route_name = 'home', renderer = 'templates/home.pt')
    def home(self):
        out = ""

        if self.request.authenticated_userid:
            with subprocess.Popen(["ip", "addr"], stdout = subprocess.PIPE) as proc:
                proc.wait(5)
                out = proc.stdout.read()

        return {'out': out}

    @view_config(route_name = 'login', renderer = 'templates/login.pt')
    def login(self):
        import pyramid.httpexceptions as exc

        if self.request.authenticated_userid is not None:
            # Already logged in -> redirect
            return exc.HTTPFound(self.request.route_path('home'), comment = "Logged in user tried to log in")

        user_not_found_error = {
            'page_background': 'warning',
            'page_title':      _(u"Login failed"),
            'page_text':       _(u"Check username and password."),
        }

        form_user = self.request.POST.get('user')
        form_password = self.request.POST.get('password')

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

            response = exc.HTTPFound(location = self.request.route_path('home'), headers = remember(self.request, ses['userid']), comment = "Login")

            log.debug("RESPONSE = %s", vars(response))

            return response
        except UserNotFoundException as exc:
            log.debug("User '%s' not found in database", form_user)
            return user_not_found_error
        except:
            raise

        # Redirect to front page
        return exc.HTTPFound(self.request.route_path('home'))


    @view_config(route_name = 'logout', renderer= 'templates/logout.pt', permission = 'admin')
    def logout(self):
        """
        Log out
        """
        if self.request.authenticated_userid is None:
            import pyramid.httpexceptions as exc
            return exc.HTTPFound(self.request.route_path('home'), comment = "Logged out user tried to logout")

        # Redirect to front page
        import pyramid.httpexceptions as exc
        return exc.HTTPFound(self.request.route_path('login'), headers = forget(self.request))
