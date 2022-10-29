import logging
from typing import List
from fastapi import  APIRouter,Depends,Response,status,Form,UploadFile,File,Request
from pydantic import EmailStr
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
import os
import json
from typing import Optional
from routers.store_user.store_schema import Store_Employee
from common.validation import validation
import pymongo 
import json
from routers.rider import strong_password
from datetime import date,datetime
now = datetime.now()

from enum import Enum
from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID

from fastapi import Body, FastAPI

current_time = now.strftime("%H:%M:%S")
password=strong_password.password
print(password)

mongoURI = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongoURI)

db = client["tis_ecommerce_service"]
collection = db["rider"]


# collection = db["rider"]
 
class Gender(str,Enum):
    male="male"
    female="female"
    others="others"
   
class User_type(str,Enum):
    store='store_employee'

class store_status(str,Enum):
    A='A'
    I='I'
    B='B'
    D='D'
    L='L'



class Blood_group(str,Enum):
    A='A+'
    a='A-'
    B='B+'
    b='B-'
    AB='AB+'
    ab='AB-'
    O='O+'
    o='O-'

class Jobtype(str,Enum):
    fulltime='fulltime'
    partime='partime'
    contract='contract'


# mongoURI = "mongodb://localhost:27017"

# client = pymongo.MongoClient(mongoURI)

# db = client["tis_ecommerce_service"]

# collection = db["combine_table"]
router = APIRouter(
    prefix=api_version + "/store_user",
    tags=["Store User"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()

@router.post('/store',status_code=201)
async def create_rider(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Body(default="2022-06-13"),
blood_group:Blood_group=Form(),gender :  Gender = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(),ifsc_code : str = Form(),user_type : User_type = Form(),store_status : store_status = Form(),user_data=Depends(auth_handler.auth_wrapper)
,user_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    data = await request.form()
    data = dict(data)
    emp_id=[]
    userdata=user_data['id']
    print("username",user_data['id'])


    if user_image_url:
        user_image_url_video = f"./uploads/store_user/user_image/{current_time}_{user_image_url.filename}"
        if not user_image_url_video:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {'status':'error','message':'Please check the valid file location'}
        split_tup = os.path.splitext(user_image_url_video)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        with open(user_image_url_video, "wb+") as file_object:
            file_object.write(user_image_url.file.read())
    user_image_url=user_image_url_video
    if aadhar_image_url:
        aadhar_location = f"./uploads/store_user/aadhar_image/{current_time}_{aadhar_image_url.filename}"
        if not aadhar_location:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {'status':'error','message':'Please check the valid file location'}
        split_tup = os.path.splitext(aadhar_location)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        with open(aadhar_location, "wb+") as file_object:
            file_object.write(aadhar_image_url.file.read())
    aadhar_image_url=aadhar_location
    if bank_passbook_url:
        bank_passbook_location = f"./uploads/store_user/bank_passbook/{current_time}_{bank_passbook_url.filename}"
        if not bank_passbook_location:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {'status':'error','message':'Please check the valid file location'}
        split_tup = os.path.splitext(bank_passbook_location)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        with open(bank_passbook_location, "wb+") as file_object:
            file_object.write(bank_passbook_url.file.read())
    bank_passbook_url=bank_passbook_location

    firstname=validation.name_validation(firstname)
    lastname=validation.lastname_validation(lastname)
    door_number=validation.door_number(door_number)
    street_name=validation.street_name_validation(street_name)
    area=validation.area_validation(area)
    city=validation.city_validation(city)
    state=validation.city_validation(state)
    pincode=validation.pincode_validation(pincode)
    aadhar_number=validation.aadhar_validation(aadhar_number)
    # driving_license_number=validation.drivinglicense_validation(driving_license_number)
    phone=validation.mobile_validate(phone)
    alternate_phone=validation.alternatephone_validate(alternate_phone)
    account_number=validation.account_number_validation(account_number)
    ifsc_code=validation.ifsc_code_validation(ifsc_code)
    bank_name=validation.bank_name_validation(bank_name)
    branch_name=validation.branch_name_validation(branch_name)
    # RCHN-001
    if city:
        emp_city=city[:3]
    if user_type:
        emp_id.append('S')
    else:
        return {"status":'error','message':'Please check city and usertype'}
    # emp=str(emp)
    collection_count=collection.count_documents({})
    # empid=ids+1
    print("ids",collection_count)
    employee_id=str(emp_id[0]) + emp_city + '-00'+ str(collection_count+1)
    print("da",employee_id) 

    print("city",city[:3])

    result = {}
    result["personal_detail"] = {}
    result["employee_detail"]={}
    result["bank_detail"] = {}
    result['contact_detail']={}
    result['supportive_document']={}

    result["personal_detail"]["firstname"] = data['firstname']
    result["personal_detail"]["lastname"] = data['lastname']
    result["personal_detail"]["dob"] = data['dob']
    result["personal_detail"]["blood_group"] = data['blood_group']
    result["personal_detail"]["gender"] = data['gender']
    result["personal_detail"]['door_number'] = data['door_number']
    result["personal_detail"]['street_name'] = data['street_name']
    result["personal_detail"]['area'] = data['area']
    result["personal_detail"]['city'] = data['city']
    result["personal_detail"]['state'] = data['state']
    result["personal_detail"]['pincode'] = data['pincode']
    result["personal_detail"]['aadhar_number'] = data['aadhar_number']

   
    result["bank_detail"]['bank_name'] = data['bank_name']
    result["bank_detail"]['branch_name'] = data['branch_name']
    result["bank_detail"]['account_number'] = data['account_number']
    result["bank_detail"]['ifsc_code'] = data['ifsc_code']
    
    result["contact_detail"]['phone'] = data['phone']
    result["contact_detail"]['alternate_phone'] = alternate_phone


    result["contact_detail"]['email'] = data['email']
    
    result["supportive_document"]['user_image_url'] = user_image_url
    result["supportive_document"]['aadhar_image_url'] =aadhar_image_url
    result["supportive_document"]['bank_passbook_url'] =bank_passbook_url
  
    result["employee_detail"]['user_type'] = data['user_type']
    result["employee_detail"]['store_status'] = data['store_status']
    result["employee_detail"]['password'] = password
    result["employee_detail"]['created_at'] = current_time
    result["employee_detail"]['updated_at'] = current_time
    result["employee_detail"]['created_by'] = userdata
    result["employee_detail"]['updated_by'] = userdata
    result["employee_detail"]['store_id'] = userdata
    result["employee_detail"]['employee_id'] = employee_id   
    id=Store_Employee(**result).save()
    return {"status":"success","message":f"Data added Successfully!"}

# get report
@router.get('/{id}',status_code=200)
def store_single_data(id : str,response : Response):
    try:
        get_data = Store_Employee.objects(id= id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND

            return { 'status': "error","message" :f"Data not exist for this id" }

        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        del userdata[0]["_id"]
        return { 'status': "success","data" :userdata[0]}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :f"Data not exist for this id {id.strip()}"}
 
@router.get("/store/employee")
def store_employee_all_data():
    collections = db["store__employee"]
    response = collections.find({})
    data=[]
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return {"status":"success","data":data}




# #Delete User Data
@router.delete('/{id}',status_code=200)
def delete_store_employee(id : str, response : Response):
    try:
        get_data = Store_Employee.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"Data  not exist for this id" }
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        user_id = userdata[0]["_id"]
        rider_image_url=userdata[0]['supportive_document']
        for image_url,value in rider_image_url.items():
            os.remove(value)
        Store_Employee.objects(id = id).delete()
        return { 'status': "success","message" :f"Data deleted Successfully" }
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}



@router.put('/{id}')
async def  store_employee_update(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Body(default="2022-06-13"),blood_group:Blood_group=Form(),gender :  Gender = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(),ifsc_code : str = Form(),user_type : User_type = Form(),store_status : store_status = Form(),user_data=Depends(auth_handler.auth_wrapper),user_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    
    try:
        get_data = Store_Employee.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"Data  not exist for this id" }
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        user_id = userdata[0]["_id"]
        rider_image_url=userdata[0]['supportive_document']
        for image_url,value in rider_image_url.items():
            os.remove(value)
        Store_Employee.objects(id = id).delete()
        data = await request.form()
        data = dict(data)
        emp_id=[]
        userdata=user_data['id']
        print("username",user_data['id'])


        if user_image_url:
            user_image_url_video = f"./uploads/store_user/user_image/{current_time}_{user_image_url.filename}"
            if not user_image_url_video:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'status':'error','message':'Please check the valid file location'}
            split_tup = os.path.splitext(user_image_url_video)
            file_name = split_tup[0]
            file_extension = split_tup[1]
            with open(user_image_url_video, "wb+") as file_object:
                file_object.write(user_image_url.file.read())
        user_image_url=user_image_url_video
        if aadhar_image_url:
            aadhar_location = f"./uploads/store_user/aadhar_image/{current_time}_{aadhar_image_url.filename}"
            if not aadhar_location:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'status':'error','message':'Please check the valid file location'}
            split_tup = os.path.splitext(aadhar_location)
            file_name = split_tup[0]
            file_extension = split_tup[1]
            with open(aadhar_location, "wb+") as file_object:
                file_object.write(aadhar_image_url.file.read())
        aadhar_image_url=aadhar_location
        if bank_passbook_url:
            bank_passbook_location = f"./uploads/store_user/bank_passbook/{current_time}_{bank_passbook_url.filename}"
            if not bank_passbook_location:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'status':'error','message':'Please check the valid file location'}
            split_tup = os.path.splitext(bank_passbook_location)
            file_name = split_tup[0]
            file_extension = split_tup[1]
            with open(bank_passbook_location, "wb+") as file_object:
                file_object.write(bank_passbook_url.file.read())
        bank_passbook_url=bank_passbook_location

        firstname=validation.name_validation(firstname)
        lastname=validation.lastname_validation(lastname)
        door_number=validation.door_number(door_number)
        street_name=validation.street_name_validation(street_name)
        area=validation.area_validation(area)
        city=validation.city_validation(city)
        state=validation.city_validation(state)
        pincode=validation.pincode_validation(pincode)
        aadhar_number=validation.aadhar_validation(aadhar_number)
        # driving_license_number=validation.drivinglicense_validation(driving_license_number)
        phone=validation.mobile_validate(phone)
        alternate_phone=validation.alternatephone_validate(alternate_phone)
        account_number=validation.account_number_validation(account_number)
        ifsc_code=validation.ifsc_code_validation(ifsc_code)
        bank_name=validation.bank_name_validation(bank_name)
        branch_name=validation.branch_name_validation(branch_name)
        # RCHN-001
        if city:
            emp_city=city[:3]
        if user_type:
            emp_id.append('S')
        else:
            return {"status":'error','message':'Please check city and usertype'}
        # emp=str(emp)
        collection_count=collection.count_documents({})
        # empid=ids+1
        print("ids",collection_count)
        employee_id=str(emp_id[0]) + emp_city + '-00'+ str(collection_count+1)
        print("da",employee_id) 

        print("city",city[:3])

        result = {}
        result["personal_detail"] = {}
        result["employee_detail"]={}
        result["bank_detail"] = {}
        result['contact_detail']={}
        result['supportive_document']={}

        result["personal_detail"]["firstname"] = data['firstname']
        result["personal_detail"]["lastname"] = data['lastname']
        result["personal_detail"]["dob"] = data['dob']
        result["personal_detail"]["blood_group"] = data['blood_group']
        result["personal_detail"]["gender"] = data['gender']
        result["personal_detail"]['door_number'] = data['door_number']
        result["personal_detail"]['street_name'] = data['street_name']
        result["personal_detail"]['area'] = data['area']
        result["personal_detail"]['city'] = data['city']
        result["personal_detail"]['state'] = data['state']
        result["personal_detail"]['pincode'] = data['pincode']
        result["personal_detail"]['aadhar_number'] = data['aadhar_number']

    
        result["bank_detail"]['bank_name'] = data['bank_name']
        result["bank_detail"]['branch_name'] = data['branch_name']
        result["bank_detail"]['account_number'] = data['account_number']
        result["bank_detail"]['ifsc_code'] = data['ifsc_code']
        
        result["contact_detail"]['phone'] = data['phone']
        result["contact_detail"]['alternate_phone'] = alternate_phone


        result["contact_detail"]['email'] = data['email']
        
        result["supportive_document"]['user_image_url'] = user_image_url
        result["supportive_document"]['aadhar_image_url'] =aadhar_image_url
        result["supportive_document"]['bank_passbook_url'] =bank_passbook_url
    
        result["employee_detail"]['user_type'] = data['user_type']
        result["employee_detail"]['store_status'] = data['store_status']
        result["employee_detail"]['password'] = password
        result["employee_detail"]['created_at'] = current_time
        result["employee_detail"]['updated_at'] = current_time
        result["employee_detail"]['created_by'] = userdata
        result["employee_detail"]['updated_by'] = userdata
        result["employee_detail"]['store_id'] = userdata
        result["employee_detail"]['employee_id'] = employee_id   
        id=Store_Employee(**result).save()
        return {"status":"success","message":f"Data Updated Successfully!"}

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

    