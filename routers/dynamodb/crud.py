import logging,json
from fastapi import  APIRouter,Depends,Response,Request,status,Form
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
from database.connection import *
from datetime import date,datetime
from .crud_shema import todos

import boto3
from configuration.config import ACCESS_KEY_ID,SECRET_ACCESS_KEY

router = APIRouter(
    prefix=api_version + "/dynamodb",
    tags=["Dynamodb"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()


@router.post('/create',status_code=201)
def create_record(response : Response,request: Request):
    try:
        # dynamo_client = boto3.client('dynamodb',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name='ap-south-1')
        # response = dynamo_client.put_item(TableName='todos',Item={'id': {'N': "{}".format(1)},'todo_name': {'S': "{}".format('todo1')}})
        dynamo_resource=boto3.resource('dynamodb',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name='ap-south-1')
        table_name=dynamo_resource.Table('todos')
        item = {
            "id": 1,
            "todo_name": 'test2',
            "is_done": False,
            }
        response=table_name.put_item(Item=item)
        return response
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

@router.get('/list',status_code=200)
def get_records(response : Response,request: Request):
    try:
        dynamo_resource=boto3.resource('dynamodb',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name='ap-south-1')
        table_name=dynamo_resource.Table('todos')
        response = table_name.scan()
        data=response.get('Items', [])
        return data
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

@router.delete('/delete',status_code=200)
def delete_record(response : Response,request: Request):
    try:
        dynamo_resource=boto3.resource('dynamodb',aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name='ap-south-1')
        table_name=dynamo_resource.Table('todos')
        response = table_name.delete_item(Key={'id': 1})
        return response
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
