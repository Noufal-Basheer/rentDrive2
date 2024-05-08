from jose import JWTError,jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict
import os
from .schemas import TokenData,db
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
load_dotenv()


ACCESS_TOKE_EXPIRY = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET=os.getenv('SECRET_KEY')
ALGO=os.getenv('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(payload:Dict):
    to_encode = payload.copy()

    expiration_time= datetime.utcnow() + timedelta(minutes=ACCESS_TOKE_EXPIRY)
    to_encode.update({"exp":expiration_time})

    jw_token = jwt.encode(to_encode,key=SECRET,algorithm=ALGO)

    return jw_token


def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,key=SECRET,algorithms=[ALGO])
        id : str = payload.get("id")
        
        if not id:
            raise credential_exception
        
        token_data = TokenData(id=id)
        return token_data
    except JWTError as e:
        raise credential_exception


async def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code= status.HTTP_403_FORBIDDEN,
        detail="could not verify token",
        headers={"WWW-Authenticate":"Bearer"}
    )
    curr_user_id = verify_access_token(token,credential_exception).id
    current_user = await db["users"].find_one({"_id": curr_user_id})

    return current_user
