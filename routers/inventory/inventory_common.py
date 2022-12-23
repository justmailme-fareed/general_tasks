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
from .inventory_schema import store_product
from common.http_operation import get_record,get_record_count


def check_record_exists(response,collection_name,where_condtion):
    if collection_name.find_one(where_condtion):
         get_data = collection_name.find_one(where_condtion)
         data=loads(dumps(get_data))
         return { 'status': "success","data" :data}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { 'status': "error","message" :"No record found"}



def check_product_image_details(response,product_image_id):
    brand_exists=db.padmin_product_image.count_documents({'_id':ObjectId(product_image_id)})
    if brand_exists:
        get_data = db.padmin_product_image.find_one({'_id':ObjectId(product_image_id)})
        image_data=loads(dumps(get_data))
        return { 'status': "success","data" :image_data}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { 'status': "error","message" :"Product image id does not exists"}

#####
def check_product_count(parent_company_name,brand_name):
    rec_count=0
    rec_check=db.padmin_product.aggregate([{"$match":{"company_detail.parent_company":parent_company_name,"company_detail.company_brand":brand_name}},{"$project" : {"count": {'$size':"$product_detail" }}}])
    data=loads(dumps(rec_check))
    if len(data) > 0:
        rec_count=data[0]['count']
    return rec_count

####
def get_product_store_details(product_id,user_id):
    if store_product.objects.filter(product_id=product_id,store_userid=user_id):
        get_data = store_product.objects.get(product_id=product_id,store_userid=user_id)
        get_data = get_data.to_json()
        data = json.loads(get_data)
        return { 'status': "success","data" :data}
    else:
        return { 'status': "error","message" :"no records found for given Product ID"}



def check_record_mapping(product_data,response):
    try:
        parent_company_id=product_data['parent_company_id']
        brand_id=product_data['brand_id']
        product_id=product_data['product_id']
        check_parent_company=get_record_count(db.padmin_product_parent_company,{'_id':ObjectId(parent_company_id)})
        if check_parent_company == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No record found for given parent company ID {parent_company_id}"}
        check_brand_maping=get_record_count(db.padmin_product_brand,{'_id':ObjectId(brand_id),'parent_company_id':ObjectId(parent_company_id)})
        if check_brand_maping == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No mapping found for given parent company ID {parent_company_id} and brand ID {brand_id}"}
        check_product_exists=get_record_count(db.padmin_product,{'product_id':ObjectId(product_id)})
        if check_product_exists == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No product found for given product ID {product_id}"}
        check_product_mapping=get_record_count(db.padmin_product,{'product_id':ObjectId(product_id),'company_detail.parent_company_id':ObjectId(parent_company_id),'company_detail.brand_id':ObjectId(brand_id)})
        if check_product_mapping == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No mapping found for given parent company ID {parent_company_id},brand ID {brand_id} and product ID {product_id}"}
        return { 'status': "success","message" :"record found"}
    except Exception as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}
