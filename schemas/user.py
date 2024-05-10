from pydantic import BaseModel, EmailStr, Field,  field_validator
import re




from errors.exceptions import AuthException







class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    @field_validator('password')
    def validate_password(cls, password: str ):
        if not  re.match( "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})" , password):
            raise AuthException(msg= {'message': 'Choose a strong password'} , code = 422)
        return password



class UserOut(BaseModel):
    email : str 
    created_at: str
    id: int


class LoginOut(BaseModel):
    access_token: str
    expires_in : str
    user: UserOut