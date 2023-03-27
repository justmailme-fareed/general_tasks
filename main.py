"""
FileName : main.py
Description : This file has all the modules routes
Created Date : 27-03-2023
"""
from fastapi import FastAPI
from routers.address import address
import logging
import uvicorn
from database.connection import *
#Logging 
logging.basicConfig(filename='logs/eastvantage.log', filemode='w', format='%(name)s - %(levelname)s - %(module)s - %(message)s - %(asctime)s')

app = FastAPI(
    title="East vantage API",
    description="East vantage address API",
    version="v1",
)
Base.metadata.create_all(bind=engine)

app.include_router(address.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)