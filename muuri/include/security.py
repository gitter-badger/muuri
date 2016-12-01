import logging

log = logging.getLogger(__name__)

from pyramid.config import Configurator

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import SessionAuthenticationPolicy

from pyramid.security import Authenticated

from pyramid.request import Request


class AppSessionPolicy(SessionAuthenticationPolicy):
    def effective_principals(self, request: Request):
        principals = []
        if request.authenticated_userid is not None:
            principals.append(Authenticated)
            principals.append((request.authenticated_userid))
            principals.append('logged-in')
        return principals

    @staticmethod
    def groupfinder(userid, request: Request):
        groups = []
        if userid is not None:
            groups.append(Authenticated)
            groups.append(userid)
            groups.append('logged-in')
        return groups


class AppACLPolicy(ACLAuthorizationPolicy):
    pass
    # def permits(self, context, principals, permission):
    #    log.debug(context)
    #    log.debug(principals)
    #    log.debug(permission)


def includeme(config: Configurator):
    ses_policy = AppSessionPolicy(callback=AppSessionPolicy.groupfinder, debug=True)

    acl_policy = AppACLPolicy()

    config.set_authentication_policy(ses_policy)
    config.set_authorization_policy(acl_policy)
