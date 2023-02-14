from fastapi import APIRouter,Depends,Response,status
from routers.user.user_auth import AuthHandler
from configuration.config import api_version
from database.connection import *
from typing import Optional

router = APIRouter(
    prefix=api_version + "/store",
    tags=["Dashboard Home"],
    responses={404: {"description": "Not found"}},
)

auth_handler = AuthHandler()


#Dashboard Home Page
@router.get('/dashboard-home',status_code=200)
def dashboard_home_page(response : Response, search_val : Optional[str] = None,skip: int = 0, limit: int = 10,user=Depends(auth_handler.auth_wrapper)):
    return {
        "status":"success",
        "order_count_detail":{
            "total_order":12,
            "pending_order":8,
            "completed_order":8,
            "cancelled_order":8,
        },
        "count":23,
        "data":[
        {
        "sno":1,
        "order_id":"order_9A33XWu170gUtm",
        "payment_mode":"Online",
        "amount":25000,
        "no_of_product":5,
        "rider_name":"ram",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
        "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":2,
        "order_id":"order_9A33XWu170gUta",
        "payment_mode":"Online",
        "amount":35000,
        "no_of_product":6,
        "rider_name":"ram",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":3,
        "order_id":"order_9A33XWu170gUt3",
        "payment_mode":"Online",
        "amount":10000,
        "no_of_product":3,
        "rider_name":"suresh",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
        "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":4,
        "order_id":"order_9A33XWu170gUt4",
        "payment_mode":"Cash On Delivery",
        "amount":10000,
        "no_of_product":3,
        "rider_name":"suresh",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":5,
        "order_id":"order_9A33XWu170gUt5",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":6,
        "rider_name":"vikram",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":6,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":7,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":8,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
        "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":9,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":10,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":11,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":12,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":13,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":14,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":15,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":16,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":17,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":18,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":19,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":20,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":21,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":22,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        },
        {
        "sno":23,
        "order_id":"order_9A33XWu170gUt6",
        "payment_mode":"Cash On Delivery",
        "amount":4000,
        "no_of_product":7,
        "rider_name":"raju",
        "rider_profile_url":"https://tis-store-admin.s3.amazonaws.com/rider/profile/20230118004159438968.jpeg",
        "rider_phone_no":9797876787,
        "user_phone_no":8898765656,
        "action_status":"Incomplete",
         "order_date":"11 Feb 23, 10:11:12 AM"
        }
        ]
    }