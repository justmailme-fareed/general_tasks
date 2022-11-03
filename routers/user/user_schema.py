"""
FileName : user_schema.py
Description : User related schema present here.
Author : Tree Integrated services
Created Date : 30-9-2022
"""

from pydantic import BaseModel,validator
from database.connection import *
from enum import Enum
import datetime

"""Pydantic user Schema"""
class UserDetails(BaseModel):
    username: str
    password : str

    class Config:
        schema_extra = {
            "example": {
                "username": "storeuser",
                "password": "storeuser@123",
            }
        }
    #username validation
    @validator('username')
    def username_validate(cls, v):
        v = v.strip()
        if v == "":
            raise ValueError('Username field required')
        return v

    #username validation
    @validator('password')
    def password_validaate(cls, v):
        v = v.strip()
        if v == "":
            raise ValueError('Password field required')
        return v
"""Store Admin Status ENUM Values"""      
class StoreAdminStatus(Enum):
    Active = 'A'
    Inactive = 'I'
    Blocked = 'B'
    Deleted = 'D'
    Locked = 'L'

"""Store Admin Status ENUM Values"""      
class StoreAdminUserType(Enum):
    StoreAdmin = 'store_admin'


"""Db schema for Store Admin user"""
class StoreUser(Document):
    username = StringField()
    password = StringField()
    status = EnumField(StoreAdminStatus, default=StoreAdminStatus.Active)
    user_type = EnumField(StoreAdminUserType, default=StoreAdminUserType.StoreAdmin)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)



   

