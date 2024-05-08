from fastapi import APIRouter, Form,HTTPException,status
from fastapi.encoders import jsonable_encoder
from ..utils import get_password_hash
from ..schemas import User,db,UserResponse
import secrets
from fastapi import Form, status
from fastapi.responses import RedirectResponse




router = APIRouter(
    tags=["User Routes"]
)


@router.post("/registration", response_description="Register a user", response_model=UserResponse)
async def registration(user_info: User):
    user_info = jsonable_encoder(user_info)

    # check for duplication
    username_found = await db["users"].find_one({"name": user_info["name"]})
    email_found = await db["users"].find_one({"email": user_info["email"]})

    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username is already taken")
    
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email id already taken")
    user_info["password"] = get_password_hash(user_info["password"])
    user_info["apiKey"] = secrets.token_hex(30)

    new_user = await db["users"].insert_one(user_info)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
   
    return created_user



