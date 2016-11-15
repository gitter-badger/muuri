from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Sequence
from sqlalchemy import Integer
from sqlalchemy import Index
from sqlalchemy import CheckConstraint
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import TIMESTAMP

from pyramid.security import Allow

import logging

log = logging.getLogger(__name__)

from ..database import Base

class User(Base):
    __tablename__ = 'users'

    __table_args__ = (
        CheckConstraint("login ~* '^[a-z]{3,}$'", name = __tablename__ + "_chk_login"),
        CheckConstraint("login != ''", name = __tablename__ + "_chk_login_not_empty"),
        CheckConstraint("password != ''", name = __tablename__ + "_chk_pw_not_empty"),
        Index(__tablename__ + "_idx_lower_login", text("lower(login)"), unique = True),
    )

    id = Column(Integer, Sequence('users_id_seq'), primary_key = True)
    login = Column(Unicode(64), unique = True, nullable = False, server_default = text("''"))
    password = Column(Unicode(255), nullable = False, server_default = text("''"))
    added = Column(TIMESTAMP, nullable = False, server_default = text("NOW()"))


    @property
    def __acl__(self):
        return [(Allow, self.login, 'view'), ]

    def __init__(self, login = "", password = ""):
        self.login = login
        self.password = password
