from  utils.session import CreateDBSession
from errors.exceptions import AuthException
from schemas.user import UserOut

from model.user import Users
class UserController():
    @staticmethod
    def create_user(user) : 
        with CreateDBSession() as db:
            new_user = user.dict()
            new_user['password'] = Users.generate_hash_key(new_user['password'])
            print(new_user, 'this is the new user')
            user = Users(**new_user)
            new_user = db.add(user)
            db.commit()
            db.refresh(user)
            print(user)
            return user
        
    @staticmethod
    def login_user(user) ->UserOut:
        with CreateDBSession() as db:
            valid_user = Users.get_user_by_email(user.email)
            if Users.verify_key(valid_user.password, user.password):
                return {'id': valid_user.id, 'email': valid_user.email, 'created_at' : valid_user.created_at }
            
            
        
    
 
    
    