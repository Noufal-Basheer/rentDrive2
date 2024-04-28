# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# def verify_password(plain_password,hash_password):
#     return pwd_context.verify(plain_password,hash_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)

import bcrypt

def verify_password(plain_password, hash_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hash_password)

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
