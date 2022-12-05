"""
FileName : inventory_schema.py
Description : Inventory related schema present here.
Author : Tree Integrated services
Created Date : 23-11-2022
"""

from pydantic import BaseModel,Field,validator
from database.connection import *
from enum import Enum
from uuid import UUID
from typing import Union,Optional,List,Dict
from bson.objectid import ObjectId
import json
import datetime
from common.validation import validation


"""Pydantic schema for Product Invetory """
class product_inventory(BaseModel):
    product_id: str
    purchased_price: float
    selling_price: float
    in_stock_count: int
    brand_name: str
    
    @validator("product_id")
    def product_id_validation(cls, value,field):
        return validation.objectID_validate(value,"Product ID")
    @validator("purchased_price")
    def purchased_price_validation(cls, value,field):
        return validation.decimal_number_validate(value,"Purchased price")
    @validator("selling_price")
    def selling_price_validation(cls, value,field):
        return validation.decimal_number_validate(value,"Selling price")
    @validator("in_stock_count")
    def in_stock_count_validation(cls, value,field):
        return validation.decimal_number_validate(value,"In stock count")
    @validator("brand_name")
    def brand_name_validation(cls, value,field):
        return validation.text_name_validate(value,3,30,"Brand name")


class product_inventory_schema(BaseModel):
    products_list: List[product_inventory]
    class Config:
        schema_extra = {
            "example": {"products_list":
                        [{
                            "product_id": "637872d62cbfc90827960423",
                            "purchased_price": 90.00,
                            "selling_price": 100.00,
                            "in_stock_count": 10,
                            "brand_name": "aachi"
                        }]
            }
        }
        

"""Db schema for Product Invetory """
class store_product(Document):
    store_userid = ObjectIdField()
    product_common_id = ObjectIdField()
    product_id = ObjectIdField()
    purchased_price = DecimalField()
    selling_price = DecimalField()
    in_stock_count = IntField()
    brand_name = StringField()
    status = BooleanField(default=True,required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    created_by = ObjectIdField(required=True)
    updated_by = ObjectIdField(required=True)
