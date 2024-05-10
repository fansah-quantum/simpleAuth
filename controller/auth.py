from datetime import datetime, timedelta
from typing import Tuple, Union

from jose import jwt, JWTError
from fastapi import security

from config import setting
from errors.exceptions import AuthException

setting = setting.AuthSettings()



class AuthToken:
    """
    This class is used to provide
    authentication and authorization functionality
    for the third party connectivity
    """

    @staticmethod
    def encode_auth_token(email: str) -> Union[Tuple[str, int], ValueError]:
        """
        Generates the auth token
        """
        try:
            payload = {
                "exp": datetime.utcnow()
                + timedelta(minutes=setting.JWT_ACCESS_TOKEN_EXPIRE),
                "iat": datetime.utcnow(),
                "sub": email,
            }
            return (
                jwt.encode(
                    payload, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM
                ),
                setting.JWT_ACCESS_TOKEN_EXPIRE * 60,
            )
        except Exception as e:
            raise ValueError(e.args[0])

    @staticmethod
    def verify_auth_token(auth_token: str) -> str:
        """
        Verifies the auth token
        """
        try:
            payload = jwt.decode(
                auth_token, setting.JWT_SECRET_KEY, algorithms=setting.JWT_ALGORITHM
            )
            return payload["sub"]
        except JWTError:
            raise AuthException(
                msg={"message": "Signature expired. Please log in again"}, code=403
            )
        

bearerschema = security.HTTPBearer()
