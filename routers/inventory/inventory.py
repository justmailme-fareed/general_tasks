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
        brand_name=brand_name.strip()
        where_condtion={"status" :True}
        if brand_name:
            where_condtion={"name" :brand_name,"status" :True}
        record_count = get_record_count(db.padmin_product_brand,where_condtion)
        if record_count == 0:
             return { 'status': "success","message" :"No records found"}
        #{'$group':{'_id':"$product_ref_id",'company_detail':{'$first':"$company_detail"},'category_detail':{'$first':"$category_detail"},'product_detail':{'$push':{'product_id':"$product_id",'title':"$title",'description':"$description",'quantity_detail':"$quantity_detail",'price_detail':"$price_detail",'shelf_detail':'$shelf_detail','product_image_id':"$product_image_id",'thumbnail_url':"$product_img_detail.thumbnail_url",'product_image_url':"$product_img_detail.product_image_url",'hsn_number':"$hsn_number",'gst':"$gst",'status':"$status"}}}} 
        data=db.padmin_product_brand.aggregate([{'$match' :where_condtion},{'$lookup':{'from': "padmin_product_parent_company",'localField': "parent_company_id","foreignField":"_id",'as':"parent_company_detail"}},{'$unwind': "$parent_company_detail"},
        #{'$lookup':{'from': "padmin_product",'localField': "_id","foreignField":"company_detail.brand_id",'as':"product_detail"}},{'$unwind': "$product_detail"},
        #{'$group':{'_id':"$product_detail.company_detail.brand_id",'product_count':{'$sum':1}}},
        #{'$group':{'_id':"$_id",'data':{'$push':{'parent_company':{'id':"$parent_company_detail._id",'name':"$parent_company_detail.name"},"name":"$name",'logo_url':"$logo_url",'status':"$status"}}}},
        #{'$group': {'_id':"$product_detail.company_detail.brand_id",'product_count':{'$sum':1}}},
        #{'$addFields': {'product_detail': {'$size': "$product_detail" }}},
        #{'$project':{"id":"$_id",'data':'$data'}}])
        {'$project':{"id":"$_id",'parent_company':{'id':"$parent_company_detail._id",'name':"$parent_company_detail.name"},"name":"$name",'logo_url':"$logo_url",'status':"$status","_id":0}},{ "$limit": skip + limit },{ "$skip": skip }])
        records_list=loads(dumps(data))
        #records_list = get_records(db.padmin_product_brand,where_condtion,skip,limit)
        for rec in records_list:
            product_count=get_record_count(db.padmin_product,{"company_detail.brand_id":ObjectId(rec['id']),"status" :True})
            rec['product_count']=product_count
            rec['id']=str(rec['id'])
            rec['parent_company']['id']=str(rec['parent_company']['id'])
        return { 'status': "success","count":record_count,"data": records_list}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#Get Inventory Product Data
@router.get('/inventory/product',status_code=200)
def get_products(response : Response,product:Optional[str] = "",skip:int=0,limit:int=25,user=Depends(auth_handler.auth_wrapper)):
    try:
        product=product.strip()
        where_condtion={"status" :True}
        if product:
            where_condtion={"title" :product,"status" :True}
        record_count = get_record_count(db.padmin_product,where_condtion)
        if record_count == 0:
             return { 'status': "success","message" :"No records found"}
        data=db.padmin_product.aggregate([{'$match' :where_condtion},
        {'$lookup':{'from': "padmin_product_image",'localField': "product_image_id","foreignField":"_id",'as':"product_img_detail"}},{'$unwind': "$product_img_detail"},
        {'$lookup':{'from': "store_product",'localField': "product_id","foreignField":"product_id",'as':"store_detail"}},
        {'$unwind': {'path':"$store_detail",'preserveNullAndEmptyArrays': True}},
        {'$project':{'product_id':"$product_id",'product_ref_id':"$product_ref_id",'title':"$title",'thumbnail_url':"$product_img_detail.thumbnail_url",'quantity_detail':"$quantity_detail",'mrp':"$price_detail",
        "purchased_price":{'$cond': {'if': {'$ne': [ { '$type':'$store_detail.purchased_price'},'missing']},'then':'$store_detail.purchased_price','else': 0}},
        "selling_price":{'$cond': {'if': {'$ne': [ { '$type':'$store_detail.selling_price'},'missing']},'then':'$store_detail.selling_price','else': 0}},
        "in_stock_count":{'$cond': {'if': {'$ne': [ { '$type':'$store_detail.in_stock_count'},'missing']},'then':'$store_detail.in_stock_count','else': 0}},
        "sale_rate":"-",'status':'$status',"_id":0}},{ "$limit": skip + limit },{ "$skip": skip }])
        records_list=loads(dumps(data))
        for rec in records_list:
            rec['product_id']=str(rec['product_id'])
            rec['product_ref_id']=str(rec['product_ref_id'])
        
        return { 'status': "success","count":record_count,"data": records_list}
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
    
