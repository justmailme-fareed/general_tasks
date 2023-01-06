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

"""Warehouse types """
class warehouse_list(str, Enum):
    All="all",
    Store="store",
  
"""Pydantic schema for Product Invetory """
class product_inventory(BaseModel):
    product_id: str
    parent_company_id: str
    brand_id: str
    purchased_price: float
    selling_price: float
    in_stock_count: int
    
    @validator("product_id")
    def product_id_validation(cls, value):
        return validation.objectID_validate(value,"Product ID")
    @validator("parent_company_id")
    def company_id_validation(cls, value):
        return validation.objectID_validate(value,"Parent Company ID")
    @validator("brand_id")
    def brand_id_validation(cls, value):
        return validation.objectID_validate(value,"Brand ID")
    @validator("purchased_price")
    def purchased_price_validation(cls, value):
        return validation.decimal_number_validate(value,"Purchased price")
    @validator("selling_price")
    def selling_price_validation(cls, value):
        return validation.decimal_number_validate(value,"Selling price")
    @validator("in_stock_count")
    def in_stock_count_validation(cls, value):
        return validation.decimal_number_validate(value,"In stock count")
    


class product_inventory_schema(BaseModel):
    products_list: List[product_inventory]
    class Config:
        schema_extra = {
            "example": {"products_list":
                        [{
                            "product_id": "637872d62cbfc90827960423",
                            "parent_company_id": "637872d62cbfc90827960423",
                            "brand_id": "637872d62cbfc90827960423",
                            "purchased_price": 90.00,
                            "selling_price": 100.00,
                            "in_stock_count": 10,
                        }]
            }
        }
        

"""Db schema for Product Invetory """
class store_product(Document):
    store_userid = ObjectIdField()
    parent_company_id = ObjectIdField()
    brand_id = ObjectIdField()
    product_ref_id = ObjectIdField()
    product_id = ObjectIdField()
    purchased_price = DecimalField()
    selling_price = DecimalField()
    in_stock_count = IntField()
    status = BooleanField(default=True,required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    created_by = ObjectIdField(required=True)
    updated_by = ObjectIdField(required=True)
