"""
FileName : inventory.py
Description : This file manage inventory section.
Author : Tree Integrated services
Created Date : 23-11-2022
"""

from fastapi import APIRouter,Depends,Response,status,File,Request, UploadFile,Form
from routers.user.user_auth import AuthHandler
from .inventory_schema import product_inventory_schema,store_product
from .inventory_common import check_record_mapping,check_product_image_details,get_product_store_details
from common.http_operation import get_record,get_records,get_record_count
from configuration.config import api_version
from database.connection import *
from common.validation import form_validation
import logging
import json
from typing import Optional,List
import datetime
import bson
from bson.json_util import loads
from bson import ObjectId
from bson.json_util import dumps
from pydantic import parse_obj_as

router = APIRouter(
    prefix=api_version + "/store",
    tags=["Store Inventory"],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()



#Get Inventory Brand Data
@router.get('/inventory/brand',status_code=200)
def get_brands(response : Response ,brand_name:Optional[str] = "",skip:int=0,limit:int=25,user=Depends(auth_handler.auth_wrapper)):
    try:
        records=[]
        brand_name=brand_name.strip()
        where_condtion={"status" :True}
        if brand_name:
            where_condtion={"name" :brand_name,"status" :True}
        record_count = get_record_count(db.padmin_product_brand,where_condtion)
        if record_count == 0:
             return { 'status': "success","message" :"No records found"}
        records_list = get_records(db.padmin_product_brand,where_condtion,skip,limit)
        for i in records_list:
            product_count=get_record_count(db.padmin_product,{"company_detail.brand_id":ObjectId(i['_id']),"status" :True})
            parent_comp_details=get_record(db.padmin_product_parent_company,{"_id":ObjectId(i['parent_company_id'])})
            parent_company={'id':str(parent_comp_details['_id']),'name':parent_comp_details['name']}
            #records.append({"product_count":product_count,'parent_company':parent_company,"name":i['name'],"logo_url":i['logo_url'],"status":i['status']})
            records.append({"id":str(i['_id']),"product_count":product_count,'parent_company':parent_company,"name":i['name'],"logo_url":i['logo_url'],"status":i['status']})
        return { 'status': "success","count":record_count,"data": records}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#Get Inventory Product Data
@router.get('/inventory/product',status_code=200)
def get_products(response : Response,product:Optional[str] = "",skip:int=0,limit:int=25,user=Depends(auth_handler.auth_wrapper)):
    try:
        product_detail=[]
        product=product.strip()
        where_condtion={"status" :True}
        if product:
            where_condtion={"titile" :product,"status" :True}
        record_count = get_record_count(db.padmin_product,where_condtion)
        if record_count == 0:
             return { 'status': "success","message" :"No records found"}
        records_list = get_records(db.padmin_product,where_condtion,skip,limit)
        for p in records_list:
            purchased_price=0
            selling_price= 0
            in_stock=0
            product_track_message="Only few left,Hurry!"
            product_image_details=check_product_image_details(response,p['product_image_id'])
            if product_image_details['status']=="error":
                return product_image_details
            thumbnail_url=product_image_details['data']['thumbnail_url']
            product_store_data=get_product_store_details(p['product_id'],user['id'])
            if product_store_data['status']=="success":
                purchased_price= product_store_data['data']['purchased_price']
                selling_price= product_store_data['data']['selling_price']
                in_stock= product_store_data['data']['in_stock_count']
            product_detail.append(
            {
                "product_id":str(p['product_id']),
                "product_ref_id":str(p['product_ref_id']),
                "titile":p['titile'],
                "thumbanil_url":thumbnail_url,
                "quantity_detail":p['quantity_detail'],
                "mrp":p['price_detail'],
                "purchased_price":purchased_price,
                "selling_price":selling_price, 
                "in_stock_count":in_stock, 
                "sale_rate":'-',
                "status":p['status']
            })
        return { 'status': "success","count":record_count,"data": product_detail}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#Post Inventory Data
@router.post('/product-inventory', status_code=200)
async def product_inventory(response : Response,product_inventory_details:product_inventory_schema,user=Depends(auth_handler.auth_wrapper)):
    try: 
        product_data=product_inventory_details.dict()
        for p in product_data['products_list']:
            parent_company_id=p['parent_company_id']
            brand_id=p['brand_id']
            product_id=p['product_id']
            check_maping=check_record_mapping(p,response)
            if check_maping['status']=='error':
                return check_maping
            product_detail=get_record(db.padmin_product,{"product_id": ObjectId(product_id)})
            product_ref_id=product_detail['product_ref_id']
            if store_product.objects.filter(parent_company_id=parent_company_id,brand_id=brand_id,product_id=product_id,product_ref_id=product_ref_id,store_userid=user['id']):
                get_data = store_product.objects.get(parent_company_id=parent_company_id,brand_id=brand_id,product_id=product_id,product_ref_id=product_ref_id,store_userid=user['id'])
                get_data = get_data.to_json()
                data = json.loads(get_data)
                row_id=data['_id']['$oid']
                current_stock=data['in_stock_count']
                new_stock=current_stock+p['in_stock_count']
                product_arr={}
                product_arr['purchased_price']=p['purchased_price']
                product_arr['selling_price']=p['selling_price']
                product_arr['in_stock_count']=new_stock
                product_arr['updated_by']=user['id']
                product_arr['updated_at']=datetime.datetime.now()
                store_product.objects(id=row_id).update(**product_arr)
            else:
                p['product_ref_id']=product_ref_id
                p['store_userid']=user['id']
                p['created_by']=user['id']
                p['updated_by']=user['id']
                store_product(**p).save()
        return {'status': "success", "message" :"Product inventory details saved successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}
    
