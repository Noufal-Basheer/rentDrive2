from fastapi import APIRouter, Depends, HTTPException,status
from ..schemas import db,PurchasedContentResponse,PurchasedContent
from fastapi.encoders import jsonable_encoder
from .. import oauth2
import datetime
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
        print("reached here")
        ticket = await db["purchases"].insert_one(purchased_item)
        response = await db["purchases"].find_one({"_id":ticket.inserted_id})
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create ticket")
