"""
FileName : inventory.py
Description : This file manage inventory section.
Author : Tree Integrated services
Created Date : 23-11-2022
"""

from fastapi import APIRouter,Depends,Response,status,File,Request, UploadFile,Form
from routers.user.user_auth import AuthHandler
from .inventory_schema import product_inventory_schema,store_product
from .inventory_common import check_product_count,check_product_image_details,check_record_exists,get_product_store_details,get_records,get_record_count
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
def get_brands(response : Response ,parent_company_name:Optional[str] = "", brand_name:Optional[str] = "",skip:int=0,limit:int=25,user=Depends(auth_handler.auth_wrapper)):
    try:
        records=[]
        parent_company_name=parent_company_name.strip()
        brand_name=brand_name.strip()
        message="No records found"
        where_condtion={"status" :True}
        if parent_company_name !='' and brand_name !='':
            message="No record found for given parent company and brand combination"
            where_condtion={"parent_company_name" :parent_company_name,"name" :brand_name,"status" :True}
        elif parent_company_name !='' and brand_name =='':
            message="No record found for given parent company"
            where_condtion={"parent_company_name" :parent_company_name,"status" :True}
        elif parent_company_name =='' and brand_name !='':
            message="No record found for given brand"
            where_condtion={"name" :brand_name,"status" :True}
        
        record_count = get_record_count(db.padmin_product_brand,where_condtion)
        if record_count == 0:
             return { 'status': "success","message" :message}
        records_list = get_records(response,db.padmin_product_brand,where_condtion,skip,limit)
        for i in records_list:
            product_count=check_product_count(i['parent_company_name'],i['name'])
            records.append({"product_count":product_count,'parent_company_name':i['parent_company_name'],"name":i['name'],"logo_url":i['logo_url'],"status":i['status']})
        return { 'status': "success","count":record_count,"data": records}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}


#Get Inventory Product Data
@router.get('/inventory/product',status_code=200)
def get_products(response : Response,parent_company_name:str,brand_name:str,user=Depends(auth_handler.auth_wrapper)):
    try:
        parent_company_name=parent_company_name.strip()
        brand_name=brand_name.strip()
        record_count = get_record_count(db.padmin_product_brand,{"name" :brand_name,"parent_company_name" :parent_company_name,"status" :True})
        if  record_count == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :"Parent company and brand combination does not exists"}
        product_count=check_product_count(parent_company_name,brand_name)
        if product_count == 0:
            return { 'status': "success","message" :"No record found for given parent company and brand combination"}
        get_data = db.padmin_product.find_one({"company_detail.parent_company" :parent_company_name,"company_detail.company_brand" :brand_name,"status" :True},{'_id': 0})
        data=loads(dumps(get_data))
        product_detail=[]
        for p in data['product_detail']:
            purchased_price=0
            selling_price= 0
            in_stock=0
            product_image_details=check_product_image_details(response,p['product_image_id'])
            if product_image_details['status']=="error":
                return product_image_details
            thumbanil_url=product_image_details['data']['thumbanil_url']
            product_store_data=get_product_store_details(p['product_id'],user['id'])
            if product_store_data['status']=="success":
                purchased_price= product_store_data['data']['purchased_price']
                selling_price= product_store_data['data']['selling_price']
                in_stock= product_store_data['data']['in_stock_count']
            product_detail.append(
            {
                "product_id":str(p['product_id']),
                "titile":p['titile'],
                "quantity_detail":p['quantity_detail'],
                "price_detail":p['price_detail'],
                "thumbanil_url":thumbanil_url,
                "purchased_price":purchased_price,
                "selling_price":selling_price,
                "in_stock":in_stock,
                "sale_rate":"-",
                "status":p['status']
            })
        return { 'status': "success","count":product_count,"data":product_detail}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#Post Inventory Data
@router.post('/product-inventory', status_code=200)
async def product_inventory(response : Response,request: Request,product_inventory_details:product_inventory_schema,user=Depends(auth_handler.auth_wrapper)):
    try: 
        product_data=product_inventory_details.dict()
        for p in product_data['products_list']:
            product_id=p['product_id']
            product_id=p['product_id']
            brand_name=p['brand_name']
            product_id=product_id.strip()
            brand_name=brand_name.strip()
            
            check_produt_exists=check_record_exists(response,db.padmin_product,{"product_detail": {"$elemMatch": {"product_id": ObjectId(product_id)}}})
            if check_produt_exists['status']=='error':
                check_produt_exists['message']=f'Product ID {product_id} does not exists'
                return check_produt_exists
            if store_product.objects.filter(brand_name=brand_name,product_id=product_id,store_userid=user['id']):
                get_data = store_product.objects.get(brand_name=brand_name,product_id=product_id,store_userid=user['id'])
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
                p['store_userid']=user['id']
                p['created_by']=user['id']
                p['updated_by']=user['id']
                store_product(**p).save()
        return {'status': "success", "message" :"Product inventory details saved successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}
    
