import logging

log = logging.getLogger(__name__)

import transaction
import sqlalchemy.orm.exc as a_exc
from sqlalchemy import func
from ..models import ModelBase
from ..database import DBSession
from ..database import User

class UserNotFoundException(ValueError):
    pass

class UserModel(ModelBase):
    def get_user(self, login):
        ses = DBSession()
        u = None

        try:
            transaction.begin()
            u = ses.query(User).filter(User.login == login).one()
            transaction.commit()
        except a_exc.NoResultFound as exc:
            transaction.abort()
            raise UserNotFoundException(exc)
        finally:
            ses.close()

        if u is not None:
            return u

        raise UserNotFoundException()

    def get_user_count(self):
        ses = DBSession()
        transaction.begin()
        u = ses.query(func.count(User.id)).scalar()
        transaction.commit()
        ses.close()
        return u

    def create_session(self, login, password):
        u = self.get_user(login)

        password = password.encode('utf-8')
        verified = False

        try:
            import bcrypt
            verified = bcrypt.checkpw(password = password, hashed_password = u.password.encode('utf-8'))
        except Exception as exc:
            raise

        if verified != True:
            raise Exception("Coulnd't verify password hash")

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

        ses = DBSession()

        try:
            transaction.begin()
            ses.add(User(login = login, password = encrypted_pw.decode()))
            transaction.commit()
            log.debug("User added: '%s'", login)
        except Exception as exc:
            transaction.abort()
            log.debug("User add failed for user '%s'", login)
            raise
        finally:
            ses.close()

        return True
