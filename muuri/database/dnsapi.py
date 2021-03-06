import logging

from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import Unicode
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import TIMESTAMP

log = logging.getLogger(__name__)

from ..database import Base


class DnsApi(Base):
    __tablename__ = 'dnsapis'

    __table_args__ = (
        CheckConstraint("port >= 1", name=__tablename__ + "_chk_port_range_low"),
        CheckConstraint("port <= 65535", name=__tablename__ + "_chk_port_range_high"),
        CheckConstraint("apitype >= 1", name=__tablename__ + "_chk_api_type"),
        CheckConstraint("host != ''", name=__tablename__ + "_chk_host_not_empty"),
    )

    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    apitype = Column(Integer, unique=False, nullable=False, server_default=text("-1"))
    apikey = Column(Unicode(255), unique=False, nullable=False, server_default=text("''"))
    password = Column(Unicode(255), unique=False, nullable=False, server_default=text("''"))
    host = Column(Unicode(255), unique=False, nullable=False, server_default=text("''"))
    port = Column(Integer, unique=False, nullable=False, server_default=text("0"))
    added = Column(TIMESTAMP, nullable=False, server_default=text("NOW()"))

    def __init__(self, apitype: int = -1, apikey: str = "", password: str = "", host: str = "", port: int = -1):
        self.apitype = apitype
        self.apikey = apikey
        self.password = password
        self.host = host
        self.port = port
