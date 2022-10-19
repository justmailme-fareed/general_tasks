"""
FileName : rider.py
Description : This file manage rider user functionalities.
Author : Tree Integrated services
Created Date : 30-9-2022
"""

from fastapi import APIRouter,Depends,Response,status,Form
from configuration.config import api_version
from database.connection import *

router = APIRouter(
    prefix=api_version + "/rider",
    tags=["Rider"],
    responses={404: {"description": "Not found"}},
)

#Register Store User Data
@router.post('/register', status_code=201)
def register_user(response : Response,firstname: str = Form(),lastname: str = Form(), password: str = Form()):
    try:
        pass
    except:
        pass