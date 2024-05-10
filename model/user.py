from datetime import datetime
from schemas.user import User, UserOut

import sqlalchemy as sq
from passlib.context import CryptContext


from app_core import setup
from errors.exceptions import AuthException

from tools.log import Log
from utils import session as ss

context = CryptContext(["bcrypt"], deprecated="auto")
model_log = Log(__name__)


class Users(setup.Base):
    __tablename__ = "user"
    id = sq.Column(sq.Integer, primary_key=True)
    password = sq.Column(sq.String, nullable=False)
    email = sq.Column(sq.String, unique=True, nullable=False, index=True)
       
    created_at = sq.Column(sq.DateTime, default=datetime.now())
    updated_at = sq.Column(sq.DateTime, default=datetime.now())

    def __str__(self) -> str:
        return f"{self.id}-{self.email}"

    @staticmethod
    def generate_hash_key(password: str) -> str:
        encrypted_password = context.hash(password)
        return encrypted_password

    @staticmethod
    def verify_key(hash_password: str, password: str) -> bool:
        try:
            print(context.verify(hash=hash_password, secret=password))
            return context.verify(hash=hash_password, secret=password)
        except Exception as e:
            model_log.error(Users.verify_key.__name__ + " -> " + e.args[0])
            raise AuthException(msg={"message": "Invalid credentials"}, code=403)

    @staticmethod
    def get_user_by_email(email: str) -> "Users":
        with ss.CreateDBSession() as db:
            user_found = db.query(Users).filter(Users.email == email).first()
            if not user_found:
                raise AuthException(msg={"message": "User not found"}, code=401)
            return user_found
        

    