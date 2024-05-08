
from fastapi import APIRouter, Cookie,HTTPException,status

from ..schemas import User,db,UserResponse
from .. import oauth2
import secrets


from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates 
from fastapi.security import OAuth2PasswordRequestForm
from ..utils import verify_password
from fastapi import Form, status
import ast

from ..schemas import MarketContent,db
from fastapi.encoders import jsonable_encoder
from . import purchase,market_place,users,auth
router = APIRouter(
    tags=["Home Route"]
)

templates = Jinja2Templates(directory="api/templates")

@router.get("/", response_class=HTMLResponse, include_in_schema= False)
async def home(request: Request,access_token: str = Cookie(None)):
    if access_token != None:
        at = ast.literal_eval(access_token)
        try:
            curr_user = await oauth2.get_current_user(at['access_token'])
        except:
             response= RedirectResponse('/',status_code= status.HTTP_302_FOUND)
             response.delete_cookie(key="access_token")
             return response
        if curr_user:
            return templates.TemplateResponse("/home.html",{"request":request, "access_token":access_token, "curr_user":curr_user})
    return templates.TemplateResponse("/home.html",{"request":request, "access_token":access_token, "curr_user":None})
        
@router.get("/dashboard", response_class=HTMLResponse, include_in_schema= False)
async def dashboard(request: Request,access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    else:
        at = ast.literal_eval(access_token)
        try:
            curr_user = await oauth2.get_current_user(at['access_token'])
        except:
             response= RedirectResponse('/',status_code= status.HTTP_302_FOUND)
             response.delete_cookie(key="access_token")
             return response
        
        ticket =  await db["purchases"].find_one({"lentee_id":curr_user['_id']})
        if ticket:
            lender_data = await db["users"].find_one({"_id":ticket['lender_id']})
            market_entry = await db["market"].find_one({"_id":ticket['market_id']})
        else:
            ticket = lender_data = market_entry = None
        return templates.TemplateResponse("/dashboard.html",{"request":request, "access_token":access_token,"ticket":ticket, "lender_data":lender_data, "market_entry":market_entry})


@router.get("/marketplaceitems",response_class= HTMLResponse, include_in_schema= False)
async def marketplaceitems(request: Request,access_token: str = Cookie(None)):
    try:
        if access_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
        # market_content = await get_blogs()
        limit =10 
        market_content = await db["market"].find({"sold":False}).to_list(limit)

        return templates.TemplateResponse("/marketplace.html",{"request":request, "market_content":market_content, "access_token":access_token })
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error encoding data") 

@router.get("/signin", response_class=HTMLResponse, include_in_schema= False)
def login(request: Request, access_token: str = Cookie(None)):
    return templates.TemplateResponse("/login.html",{"request":request, "access_token":access_token})

@router.post("/signin",status_code=status.HTTP_200_OK)
async def signin(user_creds:OAuth2PasswordRequestForm= Depends()):
    user = await db["users"].find_one({"name":user_creds.username})

    if user and verify_password(user_creds.password,user["password"]):
        access_token = await auth.login(user_creds)
        if access_token:
            response = RedirectResponse("/",status_code= status.HTTP_302_FOUND)
            response.set_cookie(key="access_token",value=access_token, httponly=True)
            return response
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:   
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/register", response_class=HTMLResponse, include_in_schema= False)
def register(request: Request, access_token: str = Cookie(None)):
    return templates.TemplateResponse("/register.html",{"request":request, "access_token":access_token})

@router.post("/registration/nr", response_description="Register a user", response_model=None)
async def registrationnr(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    user_info = User(name=name, email=email, password=password)
    print(name,email,password)
    user_info = jsonable_encoder(user_info)

    created_user = await users.registration(user_info)
    print(created_user)

    response = RedirectResponse("/signin",status_code= status.HTTP_302_FOUND)
    return response

@router.get("/about", response_class=HTMLResponse, include_in_schema= False)
def about(request: Request, access_token: str = Cookie(None)):
    return templates.TemplateResponse("/about.html",{"request":request, "access_token":access_token})

@router.get("/newmarketpost", response_class=HTMLResponse, include_in_schema= False)
def newmarketpost(request: Request,access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
    else:
        return templates.TemplateResponse("/newmarketpost.html",{"request":request, "access_token":access_token})

@router.post("/newmarketpost", include_in_schema= False)
async def create_post(stt: str = Form(...),
    price: str = Form(...),
    lending_period: str = Form(...),access_token: str = Cookie(None)):
    market_content = MarketContent(description="description", max_size= stt, price= price, lending_period=lending_period)
    at = ast.literal_eval(access_token)
    curr_user = await oauth2.get_current_user(at['access_token'])
    print(curr_user)
    created_post= await market_place.create_server(market_content,curr_user)
        
    if created_post:
        response = RedirectResponse('/marketplaceitems',status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token",value=access_token, httponly=True)
        return response

@router.get("/paymentgate",response_class =HTMLResponse)
async def paymentgate(request: Request, id: str, access_token: str = Cookie(None)):
    market_entry = await db["market"].find_one({"_id": id})
    return templates.TemplateResponse('/paymentgate.html',{"request":request, "market_entry":market_entry,"access_token":access_token})

@router.post("/paymentverification/{id}", response_class= RedirectResponse)
async def paymentverification(request: Request, id: str, access_token: str = Cookie(None)):
    paymentverified = True 
    if paymentverified :
        at = ast.literal_eval(access_token)
        curr_user = await oauth2.get_current_user(at['access_token'])
        print(curr_user)
        ticket = await purchase.purchase_storage(id, curr_user)
        if await db["purchases"].find_one({"_id": ticket['_id']}):
            print("Ticket Created")
            return RedirectResponse('/dashboard', status_code=status.HTTP_302_FOUND)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Payment Not Verified! Please Try Again")

            
@router.get("/signout", response_class=RedirectResponse)
def signout(request: Request, access_token: str = Cookie(None)):
    if access_token is not None:
        print(access_token)
        response= RedirectResponse('/',status_code= status.HTTP_302_FOUND)
        response.delete_cookie(key="access_token")
        return response
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")



@router.get("/download", response_class = FileResponse)
async def download_tar_file():
    # Replace 'file.tar' with the name of your tar file
    file_path = "rentdrive-presetup.tar"
    return FileResponse(file_path, media_type="application/octet-stream", filename="rentdrive-presetup.tar")


# @router.get("/account", response_class=HTMLResponse, include_in_schema= False)
# def account(request: Request, access_token: str = Cookie(None)):
#     if access_token is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found")
#     else:
#         return templates.TemplateResponse("/account.html",{"request":request, "access_token":access_token})

