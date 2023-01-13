"""
FileName : user.py
Description : This file manage user functionalities.
Author : Tree Integrated services
Created Date : 30-9-2022
"""

from fastapi import APIRouter,Depends,Response,status
from .user_auth import AuthHandler
from .user_schema import UserLoginDetails,StoreUser,UserRegisterDetails
from configuration.config import api_version
from database.connection import *
import logging
import json

# db = py_conn.tis_grocery_app
# riderTable = db['rider_StoreUser']


router = APIRouter(
    prefix=api_version + "/store-admin-user",
    tags=["Store Admin User"],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()

# #Register User Data
# @router.post('/register', status_code=201)
# def store_admin_register_user(user_details: UserRegisterDetails, response : Response):
#     try:
#         check_user = StoreUser.objects(username= user_details.username)
#         if len(check_user) == 1:
#             response.status_code = status.HTTP_409_CONFLICT
#             return { 'status': "error","message" :f"{user_details.username} is already there"} 
#         user_data = dict(user_details)
#         user_data["password"] = auth_handler.get_password_hash(user_details.password)
#         StoreUser(**user_data).save()
#         return {'status': "success","message" :f"{user_details.username} Created Successfully"}
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return { 'status': "error","message" :str(e)}

#Login User Data
@router.post('/login',status_code=200)
def store_admin_login_user(user_details: UserLoginDetails, response : Response):
    try:
        storeid = user_details.storeid
        password = user_details.password
        check_count = StoreUser.objects(store_id= storeid).count()
        if check_count == 1:
            if StoreUser.objects(status= "A",store_id=storeid).count() != 1:
                response.status_code = status.HTTP_403_FORBIDDEN
                return { 'status': "error","message" :"Sorry your account is not active now"} 
            get_data = StoreUser.objects(store_id= storeid)
            get_data = get_data.to_json()
            data = json.loads(get_data)
            password = data[0]["password"]
            # return get_data
            check_user = auth_handler.verify_password(user_details.password, password)
            if check_user == True:
                token = auth_handler.encode_token(user_details.storeid)
                if data[0]["user_type"] == "store_admin":
                    admin_type = "Store Admin"
                return {"status":"success","id": data[0]["_id"]["$oid"],"store_id":data[0]["store_id"],"username":data[0]["username"],"phone":data[0]["phone"],"email":data[0]["email"],"user_type":admin_type,"token":token}
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return { 'status': "error","message" :"Invalid store id and/or password"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :"Store ID not found"}
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

