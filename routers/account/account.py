from fastapi import APIRouter,Depends,Response,status
from routers.user.user_auth import AuthHandler
from configuration.config import api_version
from database.connection import *


router = APIRouter(
    prefix=api_version + "/store",
    tags=["Account"],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()


#Login User Data
@router.get('/account',status_code=200)
def accoun_details(response : Response):
    return {
        "status":"success",
        "count":3,
        "data":[
            {
                "sno":1,
                "date":"1-1-2023",
                "cash_amount":20000,
                "online_amount":20000,
                "online_amount":20000,
                "gross_profit":20000,
                "purchase_value":39999,
                "net_profit":30000,
                "total_order":30
            },
            {
                "sno":1,
                "date":"2-1-2023",
                "cash_amount":20000,
                "online_amount":20000,
                "online_amount":20000,
                "gross_profit":20000,
                "purchase_value":39999,
                "net_profit":30000,
                "total_order":10
            },
            {
                "sno":1,
                "date":"3-1-2023",
                "cash_amount":20000,
                "online_amount":20000,
                "online_amount":20000,
                "gross_profit":20000,
                "purchase_value":39999,
                "net_profit":30000,
                "total_order":50
            }

        ]
    }