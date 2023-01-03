"""
FileName : user_schema.py
Description : User related schema present here.
Author : Tree Integrated services
Created Date : 30-9-2022
"""

from pydantic import BaseModel,validator,EmailStr
from database.connection import *
from enum import Enum
import datetime
from typing import Optional
"""Store user register schema"""
class UserRegisterDetails(BaseModel):
    username: str
    password : str
    location_url : Optional[str]
    latitude : float
    longtitude : float
    phone :str
    email : EmailStr

    class Config:
        schema_extra = {
            "example": {
                "username": "storeuser",
                "password": "storeuser@123",
                "latitude":13.0067,
                "longtitude":80.2206,
                "phone":"9889878788",
                "email":"test@gmail.com"

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


"""Pydantic user Schema"""
class UserLoginDetails(BaseModel):
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
    username = StringField(required=True)
    password = StringField(required=True)
    location_url = StringField()
    location_address = StringField()
    latitude = FloatField(required=True)
    longtitude = FloatField(required=True)
    phone = StringField(required=True)
    email = StringField(required=True)
    status = EnumField(StoreAdminStatus, default=StoreAdminStatus.Active)
    user_type = EnumField(StoreAdminUserType, default=StoreAdminUserType.StoreAdmin)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)



   

