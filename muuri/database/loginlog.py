from sqlalchemy import Column
from sqlalchemy import Sequence
from sqlalchemy import Integer
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import TIMESTAMP

import logging

log = logging.getLogger(__name__)

from ..database import Base

class LoginLog(Base):
    __tablename__ = 'loginlog'

    __table_args__ = (
        CheckConstraint("userid != -1", name = __tablename__ + "_chk_userid_not_default"),
    )

    id = Column(Integer, Sequence('loginlog_id_seq'), primary_key = True)
    userid = Column(Integer, ForeignKey("users.id"), unique = False, nullable = False, server_default = text("-1"))
    logged_at = Column(TIMESTAMP, nullable = False, server_default = text("NOW()"))

    def __init__(self, userid):
        self.userid = userid
