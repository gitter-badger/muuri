import logging

log = logging.getLogger(__name__)

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import SessionAuthenticationPolicy

def includeme(config):
    ses_policy = SessionAuthenticationPolicy(debug = True)
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(ses_policy)
    config.set_authorization_policy(authz_policy)

    log.debug("Authentication and authorization loaded")
