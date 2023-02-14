"""
FileName : main.py
Description : This file has all the modules file
Author : Tree Integrated services
Created Date : 9-8-2022
"""
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from routers.user import user 
# from routers.rider import rider
from routers.rider import rider_details
from routers.store_user import store_details
from routers.inventory import inventory
from routers.account import account
#from routers.notification import notification
from routers.dynamodb import crud
from fastapi.middleware.cors import CORSMiddleware

import logging
import uvicorn
from preload import pre_load
#Logging 
logging.basicConfig(filename='logs/store_user.log', filemode='w', format='%(name)s - %(levelname)s - %(module)s - %(message)s - %(asctime)s')

app = FastAPI(
    title="TIS Store Dashboard API",
    description="Store Dashboard API - Tree Integrated Services",
    version="v1",
    # terms_of_service="",
    # contact={
    #     "name": "Tree Integrated Services",
    #     "url": "",
    #     "email": "test@gmail.com",
    # }
)

#Middleware Function
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
# app.include_router(rider.router)
app.include_router(store_details.router)
app.include_router(rider_details.router)
app.include_router(inventory.router)
app.include_router(account.router)
#app.include_router(notification.router)
app.include_router(crud.router)

# app.mount("/uploads", StaticFiles(directory="uploads"), name="static")

#Preload function
pre_load.store_user_insert()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)