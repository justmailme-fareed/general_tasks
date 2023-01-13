"""
FileName : preload.py
Description : This file has all the pre load module file
Author : Tree Integrated services
Created Date : 5-1-2023
"""

from routers.user.user_schema import StoreUser
from routers.user.user_auth import AuthHandler

auth_handler = AuthHandler()

class pre_load:
    def store_user_insert():
        if StoreUser.objects().count() == 0:
            data = [{"username":"store1","password":auth_handler.get_password_hash("store1@123"),"latitude":13.0067,"longtitude":80.2206,"phone":"9999999999","email":"store1@gmail.com","status":"A","user_type":"store_admin","store_id":"STRCHE001"},{"username":"store2@123","password":auth_handler.get_password_hash("store2"),"latitude":8.1833,"longtitude":77.4119,"phone":"9999999999","email":"store2@gmail.com","status":"A","user_type":"store_admin","store_id":"STRCHE002"},{"username":"store3@123","password":auth_handler.get_password_hash("store3"),"latitude":12.9165,"longtitude":79.1325,"phone":"9999999999","email":"store2@gmail.com","status":"A","user_type":"store_admin","store_id":"STRCHE003"}]
            for sdata in data:
                sdata = dict(sdata)
                StoreUser(**sdata).save()

    