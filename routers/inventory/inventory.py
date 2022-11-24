"""
FileName : inventory.py
Description : This file manage inventory section.
Author : Tree Integrated services
Created Date : 23-11-2022
"""

from fastapi import APIRouter,Depends,Response,status,File,Request, UploadFile,Form
from routers.user.user_auth import AuthHandler
from .inventory_schema import product_inventory_schema,store_product
from .inventory_common import check_product_count,get_brand_record_count,check_product_image_details
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

router = APIRouter(
    prefix=api_version + "/store",
    tags=["Store Inventory"],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()


#Get Inventory Brand Data
@router.get('/inventory/brand',status_code=200)
def get_brands(response : Response ,parent_company_name:str, brand_name:Optional[str] = "",skip:int=0,limit:int=25,user=Depends(auth_handler.auth_wrapper)):
    try:
        result={}
        parent_company_name=parent_company_name.strip()
        brand_name=brand_name.strip()
        if brand_name:
            brand_count=get_brand_record_count({"name" :brand_name,"parent_company_name" :parent_company_name,"status" :True})
            if brand_count == 0:
                return { 'status': "success","message" :"No record found for given parent company and brand combination"}
            #product_count=0
            get_data = db.padmin_product_brand.find_one({"parent_company_name" :parent_company_name,"name" :brand_name,"status" :True},{'_id': 0})
            data=loads(dumps(get_data))
            product_count=check_product_count(parent_company_name,brand_name)
            record={"product_count":product_count,"name":data['name'],"logo_url":data['logo_url'],"status":data['status']}
            result = { 'status': "success","data": record}
        else:
            records=[]
            brand_count=get_brand_record_count({"parent_company_name" :parent_company_name,"status" :True})
            if brand_count ==0:
                return { 'status': "success","message" :"No record found for given parent company"}
            get_data = db.padmin_product_brand.find({"parent_company_name" :parent_company_name,"status" :True},{'_id': 0}).skip(skip).limit(limit)
            data=loads(dumps(get_data))
            for i in data:
                product_count=check_product_count(parent_company_name,i['name'])
                records.append({"product_count":product_count,"name":i['name'],"logo_url":i['logo_url'],"status":i['status']})
                result = { 'status': "success","count":brand_count,"data": records}
        return result
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
        brand_count=get_brand_record_count({"name" :brand_name,"parent_company_name" :parent_company_name,"status" :True})
        if  brand_count == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :"Parent company and brand combination does not exists"}
        product_count=check_product_count(parent_company_name,brand_name)
        if product_count == 0:
            return { 'status': "success","message" :"No record found for given parent company and brand combination"}
        get_data = db.padmin_product.find_one({"company_detail.parent_company" :parent_company_name,"company_detail.company_brand" :brand_name,"status" :True},{'_id': 0})
        data=loads(dumps(get_data))
        product_detail=[]
        for p in data['product_detail']:
            product_image_details=check_product_image_details(response,p['product_image_id'])
            if product_image_details['status']=="error":
                return product_image_details
            thumbanil_url=product_image_details['data']['thumbanil_url']
            product_detail.append(
            {
                "product_id":str(p['product_id']),
                "titile":p['titile'],
                "quantity_detail":p['quantity_detail'],
                "price_detail":p['price_detail'],
                "thumbanil_url":thumbanil_url,
                "purchased_price":0,
                "selling_price":0,
                "in_stock":0,
                "sale_rate":"-",
                "in_stock":0,
                "status":p['status']
            })
        return { 'status': "success","count":product_count,"data":product_detail}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#Post Inventory Data
@router.post('/product-inventory', status_code=201)
async def product_inventory(response : Response,request: Request,product_inventory_details: List[product_inventory_schema],user=Depends(auth_handler.auth_wrapper)):
    try: 
        get_data = product_inventory_details.to_json()
        data = json.loads(get_data)
        raise SystemExit(data)
        product_data=product_inventory_details.dict()
        raise SystemExit(product_data)
        product_id=product_data['product_id']
        brand_name=product_data['brand_name']
        product_id=product_id.strip()
        brand_name=brand_name.strip()
        if store_product.objects.filter(brand_name=brand_name,product_id=product_id,store_userid=user['id']):
            get_data = store_product.objects.get(brand_name=brand_name,product_id=product_id,store_userid=user['id'])
            get_data = get_data.to_json()
            data = json.loads(get_data)
            row_id=data['_id']['$oid']
            product_data['updated_by']=user['id']
            product_data['updated_at']=datetime.datetime.now()
            store_product.objects(id=row_id).update(**product_data)
        else:
            product_data['padmin_id']=user['id']
            product_data['created_by']=user['id']
            product_data['updated_by']=user['id']
            store_product(**product_data).save()
        return {'status': "success", "message" :"Product inventory details saved successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}
    
