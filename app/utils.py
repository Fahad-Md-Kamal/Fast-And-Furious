from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_pwd(password:str):
    """ Make Hash of the password """
    return pwd_context.hash(password)

def verify_pwd(plain_password, hashed_password):
    """ Validate user password """
    return pwd_context.verify(plain_password, hashed_password)