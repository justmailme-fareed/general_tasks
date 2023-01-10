"""
FileName : file_upload.py
Description : This file manage user files upload.
Author : Tree Integrated services
Created Date : 01-10-2022
"""

from fastapi import APIRouter,Depends,Response,status,File, UploadFile
from fastapi.exceptions import HTTPException
import logging
import json
from PIL import Image
import datetime
import os
import boto3
from configuration.config import ACCESS_KEY_ID,SECRET_ACCESS_KEY,IMAGE_QUALITY
import logging
from botocore.exceptions import ClientError,NoCredentialsError
import pathlib
import requests
from io import BytesIO  

###################################################### File Upload Section ########################################################
image_types=['image/png','image/jpeg','image/jpg']
image_sizes=['1680X280','1240X1240','64X64','1280X1280','1024X1024','1500X600']
s3_region="ap-south-1"
max_size = 1000000
today = datetime.datetime.now()

def validate_image_name(file_detail):
    split_tup = os.path.splitext(file_detail)
    file_extension = split_tup[1]
    file_name = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')+file_extension
    return file_name

async def validate_uploaded_image(response,image_file,file_size):
    #file_size = await image_file.read()
    if len(file_size) == 0:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { 'status': "error","message" :f"Invalid file size, file size is 0"}
    if image_file.content_type not in image_types:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return { 'status': "error","message" :f"only {image_types} type allowed"}
    return { 'status': "success","image" :image_file}


###################################################### S3 Bucket Upload Section ########################################################
def connect_s3(type):
    try:
        if type=='client':
            s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        else:
            s3_client = boto3.resource('s3',aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key= SECRET_ACCESS_KEY)
        return s3_client
    except NoCredentialsError:
        return { 'status': "error","message" :"Invalid Credentials"}

def create_file_upload_bucket(bucket_name,region=None):
    try:
        s3_client = connect_s3('client')
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error("Exception occurred", exc_info=True)
        return { 'status': "error","message" :str(e)}

async def validate_and_upload_image_s3(response,bucket_name,image_file,file_location): 
    try:
        file_size = await image_file.read()
        validate_image= await validate_uploaded_image(response,image_file,file_size)
        if validate_image['status']=='error':
            return validate_image
        file_name=validate_image_name(image_file.filename)
        #image_url=image.split(s3_product_image_dir)
        s3_client = connect_s3('client')
        s3_resource = connect_s3('resource')
        bucket = s3_resource.Bucket(bucket_name)
        if not bucket.creation_date:
                create_file_upload_bucket(bucket_name,s3_region)
        img_resized = Image.open(image_file.file)
        if img_resized.mode in ("RGBA", "P"): 
            img_resized = img_resized.convert("RGB") 
        actual_image = BytesIO()
        img_resized = img_resized.resize((300,250),Image.ANTIALIAS)
        img_resized.save(actual_image, 'JPEG', quality=IMAGE_QUALITY,optimize=True)
        actual_image.seek(0)
        s3_client.upload_fileobj(actual_image,bucket_name,file_location+file_name, ExtraArgs={"ACL": "public-read",'ContentType': 'multerS3.AUTO_CONTENT_TYPE'})
        uploaded_file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_location+file_name}"
        return { 'status': "success","uploaded_file_url" :uploaded_file_url}
    except FileNotFoundError:
        return { 'status': "error","message" :"unnable to upload file to S3 bucket"}


def validate_and_delete_image_s3(bucket_name,file_location): 
    try:
        s3_resource = connect_s3('resource')
        bucket = s3_resource.Bucket(bucket_name)
        is_exists = list(bucket.objects.filter(Prefix=file_location))
        if len(is_exists) > 0:
            bucket.objects.filter(Prefix=file_location).delete()
            return { 'status': "success","message" :'file deleted successfully'}
        else:
            return { 'status': "error","message" :"file not found"}
    except FileNotFoundError:
        return { 'status': "error","message" :"unnable to delete file from S3 bucket"}

def validate_and_delete_dimension_images(bucket,file_location): 
    try:
        file_name=os.path.basename(file_location)
        folder_path=file_location.split(file_name)
        for sizes in image_sizes:
            file_size_location=folder_path[0]+sizes+'/'+file_name
            is_exists = list(bucket.objects.filter(Prefix=file_size_location))
            if len(is_exists) > 0:
                bucket.objects.filter(Prefix=file_size_location).delete()
        return { 'status': "success","message" :'file deleted successfully'}
    except FileNotFoundError:
        return { 'status': "error","message" :"unnable to delete file from S3 bucket"}