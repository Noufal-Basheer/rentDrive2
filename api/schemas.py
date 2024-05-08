import motor.motor_asyncio
from dotenv import load_dotenv 
import os
from typing import Any, Dict, Annotated, Callable
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import BaseModel,Field, EmailStr,GetJsonSchemaHandler
load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))

db = client.rentDrive_test1

class _ObjectIdPydanticAnnotation:
 
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )

PyObjectId = Annotated[
    ObjectId, _ObjectIdPydanticAnnotation
]


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra= {
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "password": "secret_code"
            }
        }

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com"
            }
        }


class TokenData(BaseModel):
    id : str

class MarketContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    description: str = Field(...)
    max_size:str = Field(...)
    lending_period:str = Field(...)
    price: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra= {
            "example": {
                "description": "description",
                "max_size":"max_size",
                "lending_period":"30 days"
            }
        }
class MarketContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    lender_name:str = Field(...)
    description: str = Field(...)
    ip_address : str = Field(...)
    lender_id : str = Field(...)
    created_at : str = Field(...)
    max_size : str = Field(...)
    lending_period:str = Field(...)
    price:str = Field(...)
    presetup_done:bool=Field(...)
    sold:bool=Field(...)
    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra= {
            "example": {
                "lender_name": "lender_name",
                "description": "description",
                "ip_address" : "ip_address",
                "lender_id" : "lender_id",
                "created_at"  : "date created ",
                "max_size":"50000000",
                "lending_period":"30 days",
                "price":"500",
                "presetup_done":"verify if presetup done",
                "sold":"verify if already taken"

            }
        }

class PurchasedContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    market_id:str = Field(...)
    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra= {
            "example": {
                "market_id": "12345",
            }
        }

class PurchasedContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    lender_id:str = Field(...)
    lentee_id:str = Field(...)
    market_id:str = Field(...)
    purchased_at:str = Field(...)
    remaining_storage:str = Field(...)
    end_date:str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra= {
            "example": {
                "lender_id": "lender_id",
                "lentee_id":"lentee_id",
                "market_id":"id of the listed item",
                "purchased_at":"date created",
                "remaining_storage":"storage available to use",
                "end_date":"contract ending time"
            }
        }