from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..utils import verify_password
from ..schemas import db
from ..oauth2 import create_access_token
router = APIRouter(
    prefix="/login",
    tags=["Authentication"]

)

@router.post("",status_code=status.HTTP_200_OK)
async def login(user_creds:OAuth2PasswordRequestForm= Depends()):
    print(user_creds)
    user = await db["users"].find_one({"name":user_creds.username})
    print(user)

    if user and verify_password(user_creds.password,user["password"]):
        access_token = create_access_token({"id": user["_id"]})

        return ({"access_token":access_token,"token_type":"bearer"})
    else:   
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)