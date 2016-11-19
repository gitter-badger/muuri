import logging

log = logging.getLogger(__name__)

import transaction
import sqlalchemy.orm.exc as a_exc
from sqlalchemy import func

from ..models import ModelBase
from ..database import DnsApi


class DnsApiNotFoundException(ValueError):
    pass

class DnsApiTypeNotFoundException(ValueError):
    pass


class DnsApiModel(ModelBase):
    def get_api_id(self, id: int):
        u = None

        try:
            u = self.ses.query(DnsApi).filter(DnsApi.id == id).one()
        except a_exc.NoResultFound as exc:
            raise DnsApiNotFoundException(exc)

        if u is not None:
            return u

        raise DnsApiNotFoundException()

    def get_api_types(self):
        return DnsApi.get_api_types()


    def add_api(self, apikey:str = "", host: str = "127.0.0.1", port: int = -1, password: str = ""):

        api_ids = self.get_api_types().keys()
        if apikey not in api_ids:
            raise DnsApiTypeNotFoundException()

        try:
            transaction.begin()
            self.ses.add(DnsApi(apikey = apikey, password = password, host = host, port = port))
            transaction.commit()
            log.debug("DNS API added")
        except Exception as exc:
            transaction.abort()
            log.debug("DNS API add failed")
            raise exc

        return True

    def list_all(self):
        u = DnsApi.query.all()
        return u