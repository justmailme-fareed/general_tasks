"""
FileName : address_schema.py
Description : address related schema present here.
Created Date : 27-03-2023
"""


from database.connection import *
from sqlalchemy import TIMESTAMP, Column, String, Integer,Float
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from pydantic import BaseModel,Field,validator
from common.validation import validation

"""Db schema for User address """
class user_address(Base):
    __tablename__ = 'user_address'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

"""Pydantic schema for User address """
class user_address_schema(BaseModel):
    address: str
    latitude: float
    longitude: float

    @validator("address")
    def user_name_validation(cls, value):
        return validation.address_validation(value,3,40,"address")
    @validator("latitude","longitude")
    def lat_long_validation(cls, value):
        return validation.lat_long_number_validation(value)
    class Config:
        schema_extra = {
            "example": {
                        "address": "jayanagar metro",
                        "latitude": 12.9295069,
                        "longitude": 77.5801653,
                        
            }
        }


