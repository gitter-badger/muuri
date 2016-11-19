import logging

log = logging.getLogger(__name__)

from ..database import DBSession

class ModelBase():
    ses = DBSession()

    def __call__(self, *args, **kwargs):
        log.debug("Calling: %s", args)
        self.ses = DBSession()

    def __init__(self):
        self.ses = DBSession()


from .user import UserModel
from .user import UserNotFoundException
from .loginlog import LoginLogModel
from .dnsapi import DnsApiModel