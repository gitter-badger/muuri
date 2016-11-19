import logging

log = logging.getLogger(__name__)

import transaction
import sqlalchemy.orm.exc as a_exc
from sqlalchemy import func

from ..models import ModelBase
from ..database import User

class UserNotFoundException(ValueError):
    pass

class UserModel(ModelBase):
    def get_user(self, login):
        u = None

        try:
            u = self.ses.query(User).filter(User.login == login).one()
        except a_exc.NoResultFound as exc:
            raise UserNotFoundException(exc)

        if u is not None:
            return u

        raise UserNotFoundException()

    def get_user_count(self):
        u = self.ses.query(func.count(User.id)).scalar()
        return u

    def create_session(self, login, password):
        u = None

        try:
            u = self.get_user(login)
        except:
            raise

        if u is None:
            raise UserNotFoundException()

        password = password.encode('utf-8')
        verified = False

        try:
            import bcrypt
            verified = bcrypt.checkpw(password = password, hashed_password = u.password.encode('utf-8'))
        except Exception as exc:
            raise

        if verified != True:
            raise Exception("Coulnd't verify password hash")

        from ..models import LoginLogModel

        return {'userid': u.id}

    def add_user(self, login, password):
        password = password.encode('utf-8')

        import bcrypt
        encrypted_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        verified = False

        try:
            verified = bcrypt.checkpw(password = password, hashed_password = encrypted_pw)
        except Exception:
            raise

        if verified != True:
            raise Exception("Coulnd't verify password hash")

        try:
            transaction.begin()
            self.ses.add(User(login = login, password = encrypted_pw.decode()))
            transaction.commit()
            log.debug("User added: '%s'", login)
        except Exception as exc:
            transaction.abort()
            log.debug("User add failed for user '%s'", login)
            raise

        return True
