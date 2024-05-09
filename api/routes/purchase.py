from fastapi import APIRouter, Depends, HTTPException,status
from ..schemas import db,PurchasedContentResponse,UpdatePurchasedContent
from fastapi.encoders import jsonable_encoder
from .. import oauth2
import datetime
from bson import ObjectId
from typing import List
router = APIRouter(
    prefix="/purchase",
    tags=["Add "]
)


@router.post("/{id}", response_model=PurchasedContentResponse)
async def purchase_storage(id: str, current_user=Depends(oauth2.get_current_user)):
    try:
        market_item = await db["market"].find_one({"_id": id})
        print(market_item)
        if market_item["sold"]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Already in use")
        if market_item["lender_id"] == current_user["_id"]:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Lender and lentee cannot be same")
        
        purchased_item = {
            "lentee_id": current_user["_id"],
            "lender_id": market_item["lender_id"],
            "market_id": market_item["_id"],
            "purchased_at": str(datetime.datetime.utcnow()),
            "remaining_storage": market_item["max_size"],
            "end_date": str(datetime.datetime.utcnow() + datetime.timedelta(days=30))
        }

        ticket = await db["purchases"].insert_one(jsonable_encoder(purchased_item))
        await db["market"].update_one({"_id": id}, {"$set": {"sold": True}})
        response = await db["purchases"].find_one({"_id":ticket.inserted_id})
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create ticket")


@router.get("/id",response_model=PurchasedContentResponse)
async def get_ticket_for_currentuser(current_user=Depends(oauth2.get_current_user)):
    try:
        ticket  = await db["purchases"].find_one({"lentee_id":current_user["_id"]})
        if not ticket:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No tickets found")
        return ticket
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to find ticket")


@router.get("/ip_address",response_model=str)
async def get_ticket_for_currentuser(id:str,current_user=Depends(oauth2.get_current_user)):
    try:
        lender_id = id
        if len(id) < 23:
            ticket  = await db["purchases"].find_one({"lentee_id":current_user["_id"]})
            lender_id = ticket["lender_id"]
        
        lender_data = await db["market"].find_one({"lender_id":lender_id})
       
        if not lender_data:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Colud not retrieve ip_address of lender. No lener found in given id")
        return lender_data["ip_address"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Colud not retrieve ip_address of lender")


@router.put("/remaining_size")
async def update_remainig_size(data:UpdatePurchasedContent,current_user=Depends(oauth2.get_current_user) ):
    try:
        current_ticket = await db["purchases"].find_one({"_id":ObjectId(data.ticket_id),"lentee_id":current_user["_id"]})
        print(current_ticket)
        current_size = current_ticket["remaining_storage"]
        if int(current_size)<int(data.size):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Storage is full. Please pull the existing files first")
        if not current_ticket:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Colud not retrieve ticket details. try again later")

        await db["purchases"].update_one({"_id":current_ticket["_id"]}, {"$set": {"remaining_storage": str(int(current_size)-int(data.size))}})
        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error Occured")
    