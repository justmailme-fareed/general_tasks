"""
FileName : aws_service_connection.py
Description : This file manage aws service access.
Author : Tree Integrated services
Created Date : 08-02-2023
"""

import logging,os,json,pathlib
import boto3
from configuration.config import ACCESS_KEY_ID,SECRET_ACCESS_KEY,AWS_REGION
import logging
from botocore.exceptions import ClientError,NoCredentialsError



###################################################### AWS Connection Details ########################################################
def connect_aws_service(request_type,service_type):
    try:
        if request_type=='client':
            service_details = boto3.client(service_type,aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name=AWS_REGION)
        else:
            service_details = boto3.resource(service_type,aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name=AWS_REGION)
        return service_details
    except NoCredentialsError:
        return { 'status': "error","message" :"Invalid Credentials"}