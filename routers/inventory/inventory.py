"""
FileName : inventory.py
Description : This file manage inventory section.
Author : Tree Integrated services
Created Date : 23-11-2022
"""

from fastapi import APIRouter,Depends,Response,status,File,Request, UploadFile,Form
from routers.user.user_auth import AuthHandler
from .inventory_schema import product_inventory_schema,store_product
from .inventory_common import check_product_image_details,check_record_exists,get_product_store_details,get_records,get_record_count,get_record
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
            product_count=get_record_count(db.padmin_product,{"company_detail.parent_company":i['parent_company_name'],"company_detail.company_brand":i['name'],"status" :True})
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
        product_count=get_record_count(db.padmin_product,{"company_detail.parent_company":parent_company_name,"company_detail.company_brand":brand_name,"status" :True})
        if product_count == 0:
            return { 'status': "success","message" :"No record found for given parent company and brand combination"}
        #product_count=get_records(db.padmin_product,{"company_detail.parent_company":parent_company_name,"company_detail.company_brand":brand_name,"status" :True})
        

        # #pdata=db.padmin_product.aggregate([{'$match' :{"company_detail.parent_company":parent_company_name,"company_detail.company_brand":brand_name,"status" :True}},{'$group' : {'_id' : "$product_common_id",'count': { '$sum': 1 }}}])
        # pdata=db.padmin_product.aggregate([{'$match' :{"company_detail.parent_company":parent_company_name,"company_detail.company_brand":brand_name,"status" :True}},{'$group' : {'_id' : "$product_common_id",'products': { '$push': "$$ROOT" },'count': { '$sum': 1 }}}])
        # datap=loads(dumps(pdata))
        # raise SystemExit(datap)

        get_data = db.padmin_product.find({"company_detail.parent_company" :parent_company_name,"company_detail.company_brand" :brand_name,"status" :True})
        data=loads(dumps(get_data))
        product_detail=[]
        for p in data:
            purchased_price=0
            selling_price= 0
            in_stock=0
            saving_price=0
            offer_percentage=0
            special_offer_percentage=0
            product_image_details=check_product_image_details(response,p['product_image_id'])
            if product_image_details['status']=="error":
                return product_image_details
            thumbanil_url=product_image_details['data']['thumbanil_url']
            product_store_data=get_product_store_details(p['product_id'],user['id'])
            if product_store_data['status']=="success":
                purchased_price= product_store_data['data']['purchased_price']
                selling_price= product_store_data['data']['selling_price']
                in_stock= product_store_data['data']['in_stock_count']
                saving_price=selling_price-purchased_price
                offer_percentage= (saving_price/selling_price)*100
            price_detail={"purchased_price":purchased_price,"selling_price":selling_price,"saving_price":saving_price,"offer_percentage":int(offer_percentage)}
            product_detail.append(
            {
                "product_id":str(p['product_id']),
                "titile":p['titile'],
                "thumbanil_url":thumbanil_url,
                "quantity_detail":p['quantity_detail'],
                "price_detail":price_detail,
                #"in_stock":in_stock,
                "special_offer_percentage":special_offer_percentage, 
                "rating":0, 
                "brand":p['company_detail']['company_brand'], 
                "in_stock":True, 
                "is_saved":False, 
                "notify_me":False, 
                "product_track_message":"Only few left,Hurry!"
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
            brand_name=p['brand_name']
            product_id=product_id.strip()
            brand_name=brand_name.strip()
            check_produt_exists=check_record_exists(response,db.padmin_product,{"product_id": ObjectId(product_id)})
            if check_produt_exists['status']=='error':
                check_produt_exists['message']=f'Product ID {product_id} does not exists'
                return check_produt_exists
            product_common_id=check_produt_exists['data']['product_common_id']
            if store_product.objects.filter(brand_name=brand_name,product_id=product_id,product_common_id=product_common_id,store_userid=user['id']):
                get_data = store_product.objects.get(brand_name=brand_name,product_id=product_id,product_common_id=product_common_id,store_userid=user['id'])
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
                p['product_common_id']=product_common_id
                p['store_userid']=user['id']
                p['created_by']=user['id']
                p['updated_by']=user['id']
                store_product(**p).save()
        return {'status': "success", "message" :"Product inventory details saved successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}
    
