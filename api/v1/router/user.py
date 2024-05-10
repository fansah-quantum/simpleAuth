"""Account Router
This module defines all routing operations for a account controller
"""

from fastapi import APIRouter, Depends, responses  # type: ignore

from controller import auth
from errors import exceptions as err
from errors.exceptions import AuthException

from schemas.user import User
from model.user import Users as userModel
from controller.user import UserController


user_router = APIRouter(prefix="/user")




@user_router.post('/create/account')
def create_account(data : User):
    print(data)
    user = UserController.create_user(data)
    if user:
        print(user, 'in the router ')
        access_token, expires_in = auth.AuthToken.encode_auth_token(user.email)
        return {"access_token": access_token, "expires_in": expires_in, 'id' : user.id, 'email': user.email}




@user_router.post(
    "/token",

)
async def login_for_access_token(
    data: User,
):
    """Get Access Token
    This Api is used to generate an access
    token to perform after a user has successfully logged in 
    The payload takes:
    - username: your username
    - password: your password
    """
    user = UserController.login_user(data)
    if user:
        access_token, expires_in = auth.AuthToken.encode_auth_token(email=user['email'])
        return {"access_token": access_token, "expires_in": expires_in, 'user': user}
    return responses.JSONResponse(
        content={"message": "Invalid credentials"}, status_code=403
    )


@user_router.get('/message')
def get_message(bearer_token =Depends(auth.bearerschema)):
    auth.AuthToken.verify_auth_token(bearer_token.credentials)
    return {'message': 'this is the message'}

