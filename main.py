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
import logging
import uvicorn
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

app.include_router(user.router)
# app.include_router(rider.router)
app.include_router(store_details.router)
app.include_router(rider_details.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)