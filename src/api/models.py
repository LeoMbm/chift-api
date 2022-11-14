import datetime
import time
import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    id: uuid.UUID = Field(default=uuid.uuid4())
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field()
    password: str = Field(...)
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    updated_at: datetime.datetime = Field(default=datetime.datetime.now())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Wallace",
                "email": "jwallace@me.com",
                "created_at": "DATETIME",
                "updated_at": "DATETIME"

            }
        }


class UpdateUserModel(BaseModel):

    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr = Field(...)
    password: str = Field(...)
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    updated_at: datetime.datetime = Field(default=datetime.datetime.now())

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Wallace",
                "email": "jwallace@me.com",
                "created_at": "DATETIME",
                "updated_at": "DATETIME"

            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}