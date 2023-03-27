"""
FileName : address_schema.py
Description : address related schema present here.
Created Date : 27-03-2023
"""


from database.connection import *
from sqlalchemy import TIMESTAMP, Column, String, Integer,Float
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


"""Db schema for User address """
class user_address(Base):
    __tablename__ = 'user_address'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
