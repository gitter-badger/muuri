import logging

log = logging.getLogger(__name__)

import transaction

from ..models import ModelBase

from ..database import LoginLog


class LoginLogModel(ModelBase):
    def __init__(self):
        pass

    def add_log(self, userid: int):
        try:
            transaction.begin()
            self.ses.add(LoginLog(userid=userid))
            transaction.commit()
            log.debug("Login entry added for userid #{0}".format(userid))
        except Exception as exc:
            transaction.abort()
            log.debug("Login entry adding failed for userid #{0}".format(userid))
            raise

        return True
