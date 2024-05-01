from fastapi import APIRouter, Depends, HTTPException,status
from ..schemas import MarketContent,MarketContentResponse,db,PurchasedContentResponse,PurchasedContent
from .. import oauth2
from fastapi.encoders import jsonable_encoder


import datetime
from typing import List
router = APIRouter(
    prefix="/marketplace",
    tags=["Add "]
)



@router.post("",response_description="Create new server",response_model=MarketContentResponse)
async def create_server(market_content:MarketContent,curr_user = Depends(oauth2.get_current_user)):
    try:
        duplicate_entry = await db["market"].find_one({"lender_id":curr_user["_id"]})
        print(curr_user["_id"])
        print("Duplicate entry:", duplicate_entry)

        if duplicate_entry:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Entry already present")

        market_content = jsonable_encoder(market_content)
        market_content['lender_name'] = curr_user['name']
        market_content['lender_id'] = curr_user["_id"]
        market_content["created_at"] = str(datetime.datetime.utcnow())
        market_content["ip_address"] = "127.0.0.1"
        market_content["presetup_done"]= False
        market_content["sold"]= False

        new_market_content = await db["market"].insert_one(market_content)
        print(new_market_content.inserted_id)
        creted_post = await db["market"].find_one({"_id":new_market_content.inserted_id})

        return creted_post


    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error encoding data")
    

@router.put("/update_ip",response_description="Update ip_address",response_model=bool)
async def update_ipaddress(ip_address:str,current_user=Depends(oauth2.get_current_user)):
    try:
        market_content = await db["market"].find_one({"lender_id":current_user["_id"]})
        if market_content:
            await db["market"].update_one({"lender_id": current_user["_id"]}, {"$set": {"ip_address": ip_address}})
            return True 
        else:
            return False  
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error updating ip address")


@router.put("/presetup_done",response_description="Update ip_address",response_model=bool)
async def update_ipaddress(current_user=Depends(oauth2.get_current_user)):
    try:
        market_content = await db["market"].find_one({"lender_id":current_user["_id"]})
        if market_content:
            await db["market"].update_one({"lender_id": current_user["_id"]}, {"$set": {"presetup_done": True}})
            return True 
        else:
            return False  
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error updating database")

@router.get("",response_description="Get all servers",response_model=List[MarketContentResponse])
async def get_blogs(limit:int =4,order_by:str = "created_at"):
    try:
        market_content = await db["market"].find({"$query": {},"$orderby":{order_by:-1}}).to_list(limit)
        return market_content
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error encoding data") 
    

# @router.put("/{id}",response_model=MarketContentResponse)
# async def update_blog(id:str,blog_content:MarketContent,current_user=Depends(oauth2.get_current_user)):
    
#     if blog_post := await db["blogPost"].find_one({"_id":id}):
#         if blog_post["author_id"]== current_user["_id"]:
#             try:
#                 blog_content = {k:v for k,v in blog_content.items() if v is not None}
#             except Exception as e:
#                 print(e)
#                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="N result")



