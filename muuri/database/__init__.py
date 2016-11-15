from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension(),
        autoflush=True,
        autocommit = False,
    ),

)

Base = declarative_base()

from .user import User


