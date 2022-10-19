"""
FileName : user.py
Description : This file manage user functionalities.
Author : Tree Integrated services
Created Date : 30-9-2022
"""

from fastapi import APIRouter,Depends,Response,status
from .user_auth import AuthHandler
from .user_schema import RiderDetails,Rider
from configuration.config import api_version
from database.connection import *
import logging
import json

# db = py_conn.tis_grocery_app
# riderTable = db['rider_StoreUser']


router = APIRouter(
    prefix=api_version + "/user",
    tags=["Store User"],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()


#Register User Data
@router.post('/register', status_code=201)
def register_user(user_details: RiderDetails, response : Response):
    try:
        check_user = Rider.objects(username= user_details.username)
        if len(check_user) == 1:
            response.status_code = status.HTTP_409_CONFLICT
            return { 'status': "error","message" :f"{user_details.username} is already there"} 
        user_data = dict(user_details)
        user_data["password"] = auth_handler.get_password_hash(user_details.password)
        Rider(**user_data).save()
        return {'status': "success","message" :f"{user_details.username} Created Successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#Login User Data
@router.post('/login',status_code=200)
def login_user(user_details: RiderDetails, response : Response):
    try:
        username = user_details.username
        password = user_details.password
        check_count = Rider.objects(username= username).count()
        if check_count == 1:
            get_data = Rider.objects(username= username)
            get_data = get_data.to_json()
            data = json.loads(get_data)
            password = data[0]["password"]
            check_user = auth_handler.verify_password(user_details.password, password)
            if check_user == True:
                token = auth_handler.encode_token(user_details.username)
                return {"status":"success","token":token}
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return { 'status': "error","message" :"Invalid username and/or password"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}


# #Get User Data
# @router.get('/{id}',status_code=200)
# def get_user_data(id : str,response : Response ,username=Depends(auth_handler.auth_wrapper)):
#     try:
#         get_data = StoreEmployee.objects(id= id)
#         get_data = get_data.to_json()
#         userdata = json.loads(get_data)
#         del userdata[0]["password"]
#         return { 'status': "success","data" :userdata}
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return { 'status': "error","message" :str(e)}


# #Delete User Data
# @router.delete('/{id}',status_code=200)
# def delete_user_data(id : str, response : Response,username=Depends(auth_handler.auth_wrapper)):
#     try:
#         get_data = StoreEmployee.objects(id= id)
#         get_data = get_data.to_json()
#         userdata = json.loads(get_data)
#         username = userdata[0]["username"]
#         StoreEmployee.objects(id = id).delete()
#         return { 'status': "success","message" :f"{username} Deleted Successfully" }
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return { 'status': "error","message" :str(e)}

# #Update User data
# @router.put('/{id}',status_code=200)
# def update_user_data(id : str,user_details: StoreUserDetails,response : Response,username=Depends(auth_handler.auth_wrapper)):
#     try:
#         get_data = StoreEmployee.objects(id= id)
#         get_data = get_data.to_json()
#         userdata = json.loads(get_data)
#         username = userdata[0]["username"]
#         user_data = dict(user_details)
#         user_data["password"] = auth_handler.get_password_hash(user_details.password)
#         StoreEmployee.objects(id=id).update(**user_data)
#         return { 'status': "success","message" :f"{username} Updated Successfully" }
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return { 'status': "error","message" :str(e)}
