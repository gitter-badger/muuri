import logging

log = logging.getLogger(__name__)

from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

metadata = MetaData()

DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension(),
    ),

)

Base = declarative_base()
Base.metadata = metadata
Base.query = DBSession.query_property()

# Imports:

from .user import User
from .loginlog import LoginLog
from .dnsapi import DnsApi
