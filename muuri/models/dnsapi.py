import logging

log = logging.getLogger(__name__)

import transaction
import sqlalchemy.orm.exc as a_exc

from ..models import ModelBase
from ..database import DnsApi
from pyramid.i18n import TranslationString as _


class DnsApiNotFoundException(ValueError):
    pass


class DnsApiTypeNotFoundException(ValueError):
    pass


class DnsApiModel(ModelBase):
    @staticmethod
    def get_api_types():
        from pypdnsrest.client import PowerDnsRestApiClient

        return {
            1: {
                'name': _(u"PowerDNS"),
                'client': PowerDnsRestApiClient,
            },
        }

    @staticmethod
    def get_api_type(id: int):
        if not isinstance(id, int):
            raise TypeError(_(u"Wrong type for id: '{0!s}'. int was expected.").format(type(id)))

        api = DnsApiModel.get_api_types().get(id, None)

        if api is not None:
            return api

        raise ValueError(_(u"Not found: '{0}'").format(id))

    def get_api(self, id: int):
        """

        :param id:
        :return DnsApi:
        """
        if not isinstance(id, int):
            raise TypeError(_(u"Wrong type for id: '{0!s}'. int was expected.").format(type(id)))

        u = None

        try:
            return self.ses.query(DnsApi).filter(DnsApi.id == id).one()
        except a_exc.NoResultFound as exc:
            raise DnsApiNotFoundException(exc)

        raise DnsApiNotFoundException()

    def get_api_id(self, id: int):
        if not isinstance(id, int):
            raise TypeError(_(u"Wrong type for id: '{0!s}'. int was expected.").format(type(id)))

        u = None

        try:
            u = self.ses.query(DnsApi).filter(DnsApi.id == id).one()
            return self.get_api_type(int(u.apitype))
        except a_exc.NoResultFound as exc:
            raise DnsApiNotFoundException(exc)

        raise DnsApiNotFoundException()

    def add_api(self, apitype: int = -1, apikey: str = "", host: str = "", port: int = -1, password: str = ""):

        api_types = map(int, self.get_api_types().keys())
        if apitype not in api_types:
            raise DnsApiTypeNotFoundException()

        try:
            transaction.begin()
            self.ses.add(DnsApi(apitype=apitype, apikey=apikey, password=password, host=host, port=port))
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
