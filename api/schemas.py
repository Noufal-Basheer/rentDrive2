import motor.motor_asyncio
from dotenv import load_dotenv 
import os
from typing import Any, Dict, Annotated, Callable
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import BaseModel,Field, EmailStr,GetJsonSchemaHandler
load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))

db = client.rentDrive_test

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

class BlogContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title:str = Field(...)
    body: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra= {
            "example": {
                "title": "Blog title",
                "body": "blog content",
            }
        }
class BlogContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title:str = Field(...)
    body: str = Field(...)
    author_name : str = Field(...)
    author_id : str = Field(...)
    created_at : str = Field(...)
    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra= {
            "example": {
                "title": "Blog title",
                "body": "blog content",
                "auther_name" : "auther_name",
                "auther_id" : "auther id",
                "created_at"  : "date created "

            }
        }