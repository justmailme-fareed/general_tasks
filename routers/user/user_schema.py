"""
FileName : user_schema.py
Description : User related schema present here.
Author : Tree Integrated services
Created Date : 30-9-2022
"""

from pydantic import BaseModel
from database.connection import *


"""Pydantic user Schema"""
class UserDetails(BaseModel):
    username: str
    password : str

    class Config:
        schema_extra = {
            "example": {
                "username": "test",
                "password": "test",
            }
        }


"""Db schema for user"""
class StoreUser(Document):
    username = StringField()
    password = StringField()



   

