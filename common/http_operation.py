"""
FileName : http_operation.py
Description : This is common CRUD file
Author : Tree Integrated services
Created Date : 30-9-2022
"""
from fastapi import Response,status
import bson
from bson import ObjectId
from bson.json_util import dumps
from bson.json_util import loads


"""Common Http Operation"""
class http_operation:
    """Insert record"""
    def insert_data():
        pass

    """Update record"""
    def update_data():
        pass

    """Delete record"""
    def delete_data():
        pass

    """Get record all"""
    def get_data_all():
        pass

    """Get Particular data"""
    def get_data_particular():
        pass

############################# pymongo Query Section ############################
def check_record_exists(response,collection_name,where_condtion):
    if collection_name.find_one(where_condtion):
         get_data = collection_name.find_one(where_condtion)
         data=loads(dumps(get_data))
         return { 'status': "success","data" :data}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return { 'status': "error","message" :"No record found"}

def get_record(collection_name,where_condtion):
    data={}
    if collection_name.find_one(where_condtion):
         get_data = collection_name.find_one(where_condtion)
         data=loads(dumps(get_data))
    return data

def get_records(collection_name,where_condition,skip,limit):
    result={}
    if collection_name.find(where_condition):
         get_data = collection_name.find(where_condition).skip(skip).limit(limit)
         data=loads(dumps(get_data))
         result=data
    return result

def get_record_count(collection_name,where_condition):
    record_exists=collection_name.count_documents(where_condition)
    record_count=loads(dumps(record_exists))
    return record_count
    
    