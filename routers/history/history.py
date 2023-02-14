from fastapi import APIRouter,Depends,Response,status
from routers.user.user_auth import AuthHandler
from configuration.config import api_version
from database.connection import *
from datetime import datetime
from typing import Optional

router = APIRouter(
    prefix=api_version + "/store",
    tags=["History"],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()

current_date = datetime.today().strftime('%Y-%m-%d')

#Inventory History
@router.get('/inventory-history',status_code=200)
def inventory_history_details(response : Response,skip: int = 0, limit: int = 10,start_date: str = current_date,end_date: str = current_date,user=Depends(auth_handler.auth_wrapper)):
    return {
        "status":"success",
        "count":3,
        "data":[
            {
                "sno":1,
                "date_time":"11/02/2023 11:30 PM",
                "no_of_parent_company":10,
                "no_of_brand":20,
                "no_of_product":30,
            },
            {
                "sno":2,
                "date_time":"07/02/2023 02:30 PM",
                "no_of_parent_company":10,
                "no_of_brand":30,
                "no_of_product":50,
            },
            {
                "sno":3,
                "date_time":"08/02/2023 12:30 PM",
                "no_of_parent_company":10,
                "no_of_brand":10,
                "no_of_product":90,
            },

        ]
    }


#Order History
@router.get('/order-history',status_code=200)
def order_history_details(response : Response,skip: int = 0, limit: int = 10,start_date: str = current_date,end_date: str = current_date,search_val : Optional[str] = None,user=Depends(auth_handler.auth_wrapper)):
    return {
        "status":"success",
        "count":6,
        "data":[
            {
                "sno":1,
                "order_id":"order_9A33XWu170gUtm",
                "payment_mode":"Online",
                "order_status":"Delivered",
                "amount":1000,
                "rider_id":"Rche-002",
                "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
                "ordered_date_time":"11/02/2023 11:30 PM",
                "delivered_date_time":"11/02/2023 04:30 PM",
                "refunded_date_time":"-",
                "cancelled_date_time":"-",
            },
            {
                "sno":2,
                "order_id":"order_9A33XWu170gUtm",
                "payment_mode":"Cash On Delivery",
                "order_status":"Cancelled",
                "amount":1000,
                "rider_id":"Rche-002",
                "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
                "ordered_date_time":"11/02/2023 11:30 PM",
                "delivered_date_time":"-",
                "refunded_date_time":"-",
                "cancelled_date_time":"11/02/2023 04:30 PM",
            },
            {
                "sno":3,
                "order_id":"order_9A33XWu170gUtm",
                "payment_mode":"Cash On Delivery",
                "order_status":"Refunded",
                "amount":1000,
                "rider_id":"Rche-002",
                "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
                "ordered_date_time":"11/02/2023 11:30 PM",
                "delivered_date_time":"-",
                "refunded_date_time":"11/02/2023 04:30 PM",
                "cancelled_date_time":"-",
            },
            {
                "sno":4,
                "order_id":"order_9A33XWu170gUtm",
                "payment_mode":"Online",
                "order_status":"Delivered",
                "amount":1000,
                "rider_id":"Rche-002",
                "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
                "ordered_date_time":"11/02/2023 11:30 PM",
                "delivered_date_time":"11/02/2023 04:30 PM",
                "refunded_date_time":"-",
                "cancelled_date_time":"-",
            },
            {
                "sno":5,
                "order_id":"order_9A33XWu170gUtm",
                "payment_mode":"Cash On Delivery",
                "order_status":"Cancelled",
                "amount":1000,
                "rider_id":"Rche-002",
                "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
                "ordered_date_time":"11/02/2023 11:30 PM",
                "delivered_date_time":"-",
                "refunded_date_time":"-",
                "cancelled_date_time":"11/02/2023 04:30 PM",
            },
            {
                "sno":6,
                "order_id":"order_9A33XWu170gUtm",
                "payment_mode":"Cash On Delivery",
                "order_status":"Refunded",
                "amount":1000,
                "rider_id":"Rche-002",
                "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
                "ordered_date_time":"11/02/2023 11:30 PM",
                "delivered_date_time":"-",
                "refunded_date_time":"11/02/2023 04:30 PM",
                "cancelled_date_time":"-",
            },
        ]
    }