from pydantic import BaseModel,Field
import uuid
from .common import Pagination
from typing import Optional

"""
Pydantic Schema's are used for validating data along with serializing (JSON -> Python) 
and de-serializing (Python -> JSON). 
It does not serve as a Mongo schema validator, in other words."""



# base
class User(BaseModel):
    first_name: str #= Field(...)
    last_name: str
    email: str
    username: str


# view
class UserView(User):
    id: str = Field(default_factory=uuid.uuid4, alias="_id") #user: uuid.UUID; 


# create
class UserCreate(User):
    password: str
    password2: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "nico",
                "last_name":"garcía",
                "email":"mail@mail.com",
                "username":"u1",
                "password":1234
            }
        }





# for filtering
class UserFilter(Pagination):
    username: Optional[str] = None
    username__contains: Optional[str] = None
    email: Optional[str] = None
    email__contains: Optional[str] = None
    first_name: Optional[str] = None
    first_name__contains: Optional[str] = None
    last_name: Optional[str] = None
    last_name__contains: Optional[str] = None













def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}