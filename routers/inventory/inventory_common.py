"""
FileName : inventory_common.py
Description : This file manages inventory common functionalities.
Author : Tree Integrated services
Created Date : 23-11-2022
"""

from fastapi import Response,status
import json
from database.connection import *
import bson
from bson import ObjectId
from bson.json_util import dumps
from bson.json_util import loads


def check_product_image_details(response,product_image_id):
    brand_exists=db.padmin_product_image.count_documents({'_id':ObjectId(product_image_id)})
    if brand_exists:
        get_data = db.padmin_product_image.find_one({'_id':ObjectId(product_image_id)})
        image_data=loads(dumps(get_data))
        return { 'status': "success","data" :image_data}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { 'status': "error","message" :"Product image id does not exists"}


def check_product_count(parent_company_name,brand_name):
    rec_count=0
    rec_check=db.padmin_product.aggregate([{"$match":{"company_detail.parent_company":parent_company_name,"company_detail.company_brand":brand_name}},{"$project" : {"count": {'$size':"$product_detail" }}}])
    data=loads(dumps(rec_check))
    if len(data) > 0:
        rec_count=data[0]['count']
    return rec_count

def get_brand_record_count(where_condition):
    brand_exists=db.padmin_product_brand.count_documents(where_condition)
    brand_count=loads(dumps(brand_exists))
    return brand_count

def check_record_exists(response,collection_name,where_condtion):
    if collection_name.find_one(where_condtion):
         get_data = collection_name.find_one(where_condtion)
         data=loads(dumps(get_data))
         return { 'status': "success","data" :data}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { 'status': "error","message" :"Product ID does not exists"}

