"""
FileName : main.py
Description : This file has all the modules file
Author : Tree Integrated services
Created Date : 9-8-2022
"""

from fastapi import FastAPI
from routers.user import user 
from routers.rider import rider
import logging

#Logging 
logging.basicConfig(filename='logs/store_user.log', filemode='w', format='%(name)s - %(levelname)s - %(module)s - %(message)s - %(asctime)s')

app = FastAPI(
    title="TIS Store User API",
    description="Store User API - Tree Integrated Services",
    version="v1",
    # terms_of_service="",
    # contact={
    #     "name": "Tree Integrated Services",
    #     "url": "",
    #     "email": "test@gmail.com",
    # }
)

app.include_router(user.router)
app.include_router(rider.router)
