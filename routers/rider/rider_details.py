import logging
from typing import List
from fastapi import  APIRouter,Depends,Response,status,Form,UploadFile,File,Request
from pydantic import EmailStr
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
import os
import json
from typing import Optional
from routers.rider.rider_schema import Rider,Store
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
    rider='rider'
    store='store'
    user='user'

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
    prefix=api_version + "/rider",
    tags=["Rider"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()
# @router.post('/create', status_code=201)
# async def manufacturer(response : Response,request: Request,name : str = Form(),certificate_number:int= Form(),fssai_number:int= Form(),gst_number:str= Form(),pan_number:str= Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(), ifsc_code: str = Form(),
# contact_person : str = Form(),designation : str = Form(),phone : int = Form(),email : str = Form(),city : str = Form(),pincode : int = Form(),state : str = Form(),full_address : str = Form(),country : str = Form(),manufacturer_logo_url:UploadFile = File(...),bank_passbook:UploadFile = File(...)):
    
#     data = await request.form()

#     data = dict(data)
#     if manufacturer_logo_url:
#         video_location = f"uploads/manufacturer/image/{current_time}_{manufacturer_logo_url.filename}"
#         if not video_location:
#             response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#             return {'status':'error','message':'Please check the valid file location'}
#         split_tup = os.path.splitext(video_location)
#         file_name = split_tup[0]
#         file_extension = split_tup[1]
#         with open(video_location, "wb+") as file_object:
#             file_object.write(manufacturer_logo_url.file.read())
#     manufacturer_logo_url=video_location
#     if bank_passbook:
#         bank_passbook_location = f"uploads/manufacturer/bank/image/{current_time}_{bank_passbook.filename}"
#         if not bank_passbook_location:
#             response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#             return {'status':'error','message':'Please check the valid file location'}
#         split_tup = os.path.splitext(video_location)
#         file_name = split_tup[0]
#         file_extension = split_tup[1]
#         with open(bank_passbook_location, "wb+") as file_object:
#             file_object.write(bank_passbook.file.read())
#     bank_passbook=bank_passbook_location

    
#     name=validation.name_validation(name)
#     gst_number=validation.gst_number_validation(gst_number)
#     fssai_number=validation.fssai_number_validation(fssai_number)
#     pan_number=validation.pan_number_validation(pan_number)
#     certificate_number=validation.certificate_number_validation(certificate_number)
   
#     account_number=validation.account_number_validation(account_number)
#     ifsc_code=validation.ifsc_code_validation(ifsc_code)
#     bank_name=validation.bank_name_validation(bank_name)
#     branch_name=validation.branch_name_validation(branch_name)

#     contact_person=validation.contact_person_validation(contact_person)
#     designation=validation.designation_validation(designation)
#     phone=validation.phone_validation(phone)
#     city=validation.city_validation(city)
#     pincode=validation.pincode_validation(pincode)
#     state=validation.state_validation(state)
#     full_address=validation.fulladdress_validation(full_address)
#     country=validation.country_validation(country)
#     result = {}

#     result["manufacturer_detail"] = {}
#     result["bank_detail"] = {}
#     result['contact_detail']={}
#     result['supportive_document']={}

#     result["manufacturer_detail"]["name"] = data['name']
#     result["manufacturer_detail"]["certificate_number"] = int(data['certificate_number'])
#     result["manufacturer_detail"]["fssai_number"] = int(data['fssai_number'])
#     result["manufacturer_detail"]["gst_number"] = data['gst_number']
#     result["manufacturer_detail"]["pan_number"] = data['pan_number']

#     result["bank_detail"]['bank_name'] = data['bank_name']
#     result["bank_detail"]['branch_name'] = data['branch_name']
#     result["bank_detail"]['account_number'] = int(data['account_number'])
#     result["bank_detail"]['ifsc_code'] = data['ifsc_code']\
    
#     result["contact_detail"]['contact_person'] = data['contact_person']
#     result["contact_detail"]['designation'] = data['designation']
#     result["contact_detail"]['phone'] = int(data['phone'])
#     result["contact_detail"]['city'] = data['city']
#     result["contact_detail"]['pincode'] = data['pincode']
#     result["contact_detail"]['state'] = data['state']
#     result["contact_detail"]['full_address'] = data['full_address']
#     result["contact_detail"]['country'] = data['country']
#     result["contact_detail"]['email'] = data['email']
    
#     result["supportive_document"]['manufacturer_logo_url'] = manufacturer_logo_url
#     result["supportive_document"]['bank_passbook'] =bank_passbook
#     id=CombineTable(**result).save()
#     return {"status":"success","message":"Data added Successfully!"}

@router.post('/store',status_code=201)
async def create_rider(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Body(default="2022-06-13"),
blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Body(default="2022-06-13"),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(),ifsc_code : str = Form(),user_type : User_type = Form(),store_status : store_status = Form(),user_data=Depends(auth_handler.auth_wrapper)
,rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    data = await request.form()
    data = dict(data)
    emp_id=[]
    userdata=user_data['id']
    print("username",user_data['id'])


    if rider_image_url:
        rider_image_video = f"./uploads/rider/profile/{current_time}_{rider_image_url.filename}"
        if not rider_image_video:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {'status':'error','message':'Please check the valid file location'}
        split_tup = os.path.splitext(rider_image_video)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        with open(rider_image_video, "wb+") as file_object:
            file_object.write(rider_image_url.file.read())
    rider_image_url=rider_image_video
    if aadhar_image_url:
        aadhar_location = f"./uploads/rider/aadhar/{current_time}_{aadhar_image_url.filename}"
        if not aadhar_location:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {'status':'error','message':'Please check the valid file location'}
        split_tup = os.path.splitext(aadhar_location)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        with open(aadhar_location, "wb+") as file_object:
            file_object.write(aadhar_image_url.file.read())
    aadhar_image_url=aadhar_location
    if driving_license_url:
        driving_license_location = f"./uploads/rider/driving_license/{current_time}_{driving_license_url.filename}"
        if not driving_license_location:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {'status':'error','message':'Please check the valid file location'}
        split_tup = os.path.splitext(driving_license_location)
        file_name = split_tup[0]
        file_extension = split_tup[1]
        with open(driving_license_location, "wb+") as file_object:
            file_object.write(driving_license_url.file.read())
    driving_license_url=driving_license_location
    if bank_passbook_url:
        bank_passbook_location = f"./uploads/rider/bank_passbook/{current_time}_{bank_passbook_url.filename}"
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
    driving_license_number=validation.drivinglicense_validation(driving_license_number)
    phone=validation.mobile_validate(phone)
    alternate_phone=validation.alternatephone_validate(alternate_phone)
    account_number=validation.account_number_validation(account_number)
    ifsc_code=validation.ifsc_code_validation(ifsc_code)
    bank_name=validation.bank_name_validation(bank_name)
    branch_name=validation.branch_name_validation(branch_name)
    # RCHN-001
    if city:
        emp_city=city[:3]
    if data['user_type'] =="rider":
        emp_id.append('R')
    elif data['user_type'] =="store_user":
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
    result["driving_license_detail"] = {}
    result["employee_detail"]={}
    result["bank_detail"] = {}
    result['contact_detail']={}
    result['supportive_document']={}
    print(data['job_type'])

    result["personal_detail"]["firstname"] = data['firstname']
    result["personal_detail"]["lastname"] = data['lastname']
    result["personal_detail"]["dob"] = data['dob']
    result["personal_detail"]["blood_group"] = data['blood_group']
    result["personal_detail"]["gender"] = data['gender']
    result["personal_detail"]["language_known"] = data['language_known']
    result["personal_detail"]['door_number'] = data['door_number']
    result["personal_detail"]['street_name'] = data['street_name']
    result["personal_detail"]['area'] = data['area']
    result["personal_detail"]['city'] = data['city']
    result["personal_detail"]['state'] = data['state']
    result["personal_detail"]['pincode'] = data['pincode']
    result["personal_detail"]['aadhar_number'] = data['aadhar_number']

    result["driving_license_detail"]['driving_license_number'] = data['driving_license_number']
    result["driving_license_detail"]['driving_license_expiry_date'] = data['driving_license_expiry_date']
   
    result["bank_detail"]['bank_name'] = data['bank_name']
    result["bank_detail"]['branch_name'] = data['branch_name']
    result["bank_detail"]['account_number'] = data['account_number']
    result["bank_detail"]['ifsc_code'] = data['ifsc_code']
    
    result["contact_detail"]['phone'] = data['phone']
    result["contact_detail"]['alternate_phone'] = alternate_phone
    result["contact_detail"]['job_type'] = data['job_type']


    result["contact_detail"]['email'] = data['email']
    
    result["supportive_document"]['rider_image_url'] = rider_image_url
    result["supportive_document"]['aadhar_image_url'] =aadhar_image_url
    result["supportive_document"]['driving_license_url'] =driving_license_url
    result["supportive_document"]['bank_passbook_url'] =bank_passbook_url
   
# created_at 
# updated_at 
# created_by 
# updated_by 
# employee_id 
# store_id 
    result["employee_detail"]['user_type'] = data['user_type']
    result["employee_detail"]['store_status'] = data['store_status']
    result["employee_detail"]['password'] = password
    result["employee_detail"]['created_at'] = current_time
    result["employee_detail"]['updated_at'] = current_time
    result["employee_detail"]['created_by'] = userdata
    result["employee_detail"]['updated_by'] = userdata
    result["employee_detail"]['store_id'] = userdata
    result["employee_detail"]['employee_id'] = employee_id




   
    id=Rider(**result).save()
    return {"status":"success","message":f"Data added Successfully!"}

#get report
@router.get('/{id}',status_code=200)
def rider_single_data(id : str,response : Response):
    try:
        get_data = Rider.objects(id= id)
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
 
@router.get("/store")
def rider_all_data():
    response = collection.find({})
    data=[]
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return {"status":"success","data":data}




#Delete User Data
@router.delete('/{id}',status_code=200)
def delete_rider(id : str, response : Response):
    try:
        get_data = Rider.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"Data  not exist for this id" }
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        user_id = userdata[0]["_id"]
        rider_image_url=userdata[0]['supportive_document']
        for image_url,value in rider_image_url.items():
            os.remove(value)
        Rider.objects(id = id).delete()
        return { 'status': "success","message" :f"Data deleted Successfully" }
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

@router.put('/{id}')
async def store_update(id:str,response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Body(default="2022-06-13"),blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Body(default="2022-06-13"),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone : str = Form(),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(),ifsc_code : str = Form(),user_type : User_type = Form(),store_status : store_status = Form(),rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    try:
        get_data = Rider.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"Data  not exist for this id" }
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        user_id = userdata[0]["_id"]
        rider_image_url=userdata[0]['supportive_document']
        for image_url,value in rider_image_url.items():
            os.remove(value)
        Rider.objects(id = id).delete()
         
        data = await request.form()

        data = dict(data)
        if rider_image_url:
            rider_image_video = f"./uploads/rider/profile/{current_time}_{rider_image_url.filename}"
            if not rider_image_video:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'status':'error','message':'Please check the valid file location'}
            split_tup = os.path.splitext(rider_image_video)
            file_name = split_tup[0]
            file_extension = split_tup[1]
            with open(rider_image_video, "wb+") as file_object:
                file_object.write(rider_image_url.file.read())
        rider_image_url=rider_image_video
        if aadhar_image_url:
            aadhar_location = f"./uploads/rider/aadhar/{current_time}_{aadhar_image_url.filename}"
            if not aadhar_location:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'status':'error','message':'Please check the valid file location'}
            split_tup = os.path.splitext(aadhar_location)
            file_name = split_tup[0]
            file_extension = split_tup[1]
            with open(aadhar_location, "wb+") as file_object:
                file_object.write(aadhar_image_url.file.read())
        aadhar_image_url=aadhar_location
        if driving_license_url:
            driving_license_location = f"./uploads/rider/driving_license/{current_time}_{driving_license_url.filename}"
            if not driving_license_location:
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {'status':'error','message':'Please check the valid file location'}
            split_tup = os.path.splitext(driving_license_location)
            file_name = split_tup[0]
            file_extension = split_tup[1]
            with open(driving_license_location, "wb+") as file_object:
                file_object.write(driving_license_url.file.read())
        driving_license_url=driving_license_location
        if bank_passbook_url:
            bank_passbook_location = f"./uploads/rider/bank_passbook/{current_time}_{bank_passbook_url.filename}"
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
        driving_license_number=validation.drivinglicense_validation(driving_license_number)
        phone=validation.mobile_validate(phone)
        alternate_phone=validation.alternatephone_validate(alternate_phone)
        account_number=validation.account_number_validation(account_number)
        ifsc_code=validation.ifsc_code_validation(ifsc_code)
        bank_name=validation.bank_name_validation(bank_name)
        branch_name=validation.branch_name_validation(branch_name)
    
        result = {}
        result["personal_detail"] = {}
        result["driving_license_detail"] = {}
        result["employee_detail"]={}
        result["bank_detail"] = {}
        result['contact_detail']={}
        result['supportive_document']={}

        result["personal_detail"]["firstname"] = data['firstname']
        result["personal_detail"]["lastname"] = data['lastname']
        result["personal_detail"]["dob"] = data['dob']
        result["personal_detail"]["blood_group"] = data['blood_group']
        result["personal_detail"]["gender"] = data['gender']
        result["personal_detail"]["language_known"] = data['language_known']
        result["personal_detail"]['door_number'] = data['door_number']
        result["personal_detail"]['street_name'] = data['street_name']
        result["personal_detail"]['area'] = data['area']
        result["personal_detail"]['city'] = data['city']
        result["personal_detail"]['state'] = data['state']
        result["personal_detail"]['pincode'] = data['pincode']
        result["personal_detail"]['aadhar_number'] = data['aadhar_number']

        result["driving_license_detail"]['driving_license_number'] = data['driving_license_number']
        result["driving_license_detail"]['driving_license_expiry_date'] = data['driving_license_expiry_date']
    
        result["bank_detail"]['bank_name'] = data['bank_name']
        result["bank_detail"]['branch_name'] = data['branch_name']
        result["bank_detail"]['account_number'] = data['account_number']
        result["bank_detail"]['ifsc_code'] = data['ifsc_code']\
        
        result["contact_detail"]['phone'] = data['phone']
        result["contact_detail"]['alternate_phone'] = data['alternate_phone']
        result["contact_detail"]['job_type'] = data['job_type']
        result["contact_detail"]['email'] = data['email']
        
        result["supportive_document"]['rider_image_url'] = rider_image_url
        result["supportive_document"]['aadhar_image_url'] =aadhar_image_url
        result["supportive_document"]['driving_license_url'] =driving_license_url
        result["supportive_document"]['bank_passbook_url'] =bank_passbook_url


        result["employee_detail"]['user_type'] = data['user_type']
        result["employee_detail"]['store_status'] = data['store_status']
    
        id=Rider(**result).save()
        return {"status":"success","message":f"Data updated Successfully!"}

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}


# #get report
# @router.get('/{id}',status_code=200)
# def manufacturer_single_data(id : str,response : Response):
#     try:
#         get_data = CombineTable.objects(id= id)
#         if not get_data:
#             response.status_code = status.HTTP_404_NOT_FOUND

#             return { 'status': "error","message" :f"Data not exist for this id" }

#         get_data = get_data.to_json()
#         userdata = json.loads(get_data)
#         del userdata[0]["_id"]
#         return { 'status': "success","data" :userdata}
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return { 'status': "error","message" :f"Data not exist for this id {id.strip()}"}

# @router.get("/api/getall")
# def manufacturer_all_data():
#     response = collection.find({})
#     data=[]
#     for i in response:
#         i["_id"] = str(i["_id"])
#         data.append(i)
#     return {"status":"success","data":data}


# #Delete User Data
# @router.delete('/{id}',status_code=200)
# def delete_report(id : str, response : Response):
#     try:
#         get_data = CombineTable.objects(id=id)
#         if not get_data:
#             response.status_code = status.HTTP_404_NOT_FOUND
#             return { 'status': "error","message" :f"Data  not exist for this id" }
#         get_data = get_data.to_json()
#         userdata = json.loads(get_data)
#         user_id = userdata[0]["_id"]
#         CombineTable.objects(id = id).delete()
#         return { 'status': "success","message" :f"Data deleted Successfully" }
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return { 'status': "error","message" :str(e)}


# @router.put('/update', status_code=201)
# async def manufacturer_update(id : str,response : Response,request: Request,name : str = Form(),certificate_number:int= Form(),fssai_number:int= Form(),gst_number:str= Form(),pan_number:str= Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(), ifsc_code: str = Form(),
# contact_person : str = Form(),designation : str = Form(),phone : int = Form(),email : EmailStr = Form(),city : str = Form(),pincode : int = Form(),state : str = Form(),full_address : str = Form(),country : str = Form(),manufacturer_logo_url:UploadFile = File(...),bank_passbook:UploadFile = File(...)):
#     try:
#         get_data = CombineTable.objects(id=id)
#         if not get_data:
#             response.status_code = status.HTTP_404_NOT_FOUND
#             return { 'status': "error","message" :f"Data  not exist for this id" }
#         get_data = get_data.to_json()
#         userdata = json.loads(get_data)
#         user_id = userdata[0]["_id"]
#         CombineTable.objects(id = id).delete()
#         data = await request.form()
#         data = dict(data)
#         if manufacturer_logo_url:
#             video_location = f"uploads/manufacturer/image/{current_time}_{manufacturer_logo_url.filename}"
#             if not video_location:
#                 response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#                 return {'status':'error','message':'Please check the valid file location'}
#             split_tup = os.path.splitext(video_location)
#             file_name = split_tup[0]
#             file_extension = split_tup[1]
#             with open(video_location, "wb+") as file_object:
#                 file_object.write(manufacturer_logo_url.file.read())
#         manufacturer_logo_url=video_location
#         if bank_passbook:
#             bank_passbook_location = f"uploads/manufacturer/bank/image/{current_time}_{bank_passbook.filename}"
#             if not bank_passbook_location:
#                 response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#                 return {'status':'error','message':'Please check the valid file location'}
#             split_tup = os.path.splitext(video_location)
#             file_name = split_tup[0]
#             file_extension = split_tup[1]
#             with open(bank_passbook_location, "wb+") as file_object:
#                 file_object.write(bank_passbook.file.read())
#         bank_passbook=bank_passbook_location
       
#         name=validation.name_validation(name)
#         gst_number=validation.gst_number_validation(gst_number)
#         fssai_number=validation.fssai_number_validation(fssai_number)
#         pan_number=validation.pan_number_validation(pan_number)
#         certificate_number=validation.certificate_number_validation(certificate_number)
        
#         account_number=validation.account_number_validation(account_number)
#         ifsc_code=validation.ifsc_code_validation(ifsc_code)
#         bank_name=validation.bank_name_validation(bank_name)
#         branch_name=validation.branch_name_validation(branch_name)
       
#         contact_person=validation.contact_person_validation(contact_person)
#         designation=validation.designation_validation(designation)
#         phone=validation.phone_validation(phone)
#         city=validation.city_validation(city)
#         pincode=validation.pincode_validation(pincode)
#         state=validation.state_validation(state)
#         full_address=validation.fulladdress_validation(full_address)
#         country=validation.country_validation(country)
        
#         result = {}
#         result["manufacturer_detail"] = {}
#         result["bank_detail"] = {}
#         result['contact_detail']={}
#         result['supportive_document']={}
        
#         result["manufacturer_detail"]["name"] = data['name']
#         result["manufacturer_detail"]["certificate_number"] = int(data['certificate_number'])
#         result["manufacturer_detail"]["fssai_number"] = int(data['fssai_number'])
#         result["manufacturer_detail"]["gst_number"] = data['gst_number']
#         result["manufacturer_detail"]["pan_number"] = data['pan_number']
        
#         result["bank_detail"]['bank_name'] = data['bank_name']
#         result["bank_detail"]['branch_name'] = data['branch_name']
#         result["bank_detail"]['account_number'] = int(data['account_number'])
#         result["bank_detail"]['ifsc_code'] = data['ifsc_code']
        
#         result["contact_detail"]['contact_person'] = data['contact_person']
#         result["contact_detail"]['designation'] = data['designation']
#         result["contact_detail"]['phone'] = int(data['phone'])
#         result["contact_detail"]['city'] = data['city']
#         result["contact_detail"]['pincode'] = data['pincode']
#         result["contact_detail"]['state'] = data['state']
#         result["contact_detail"]['full_address'] = data['full_address']
#         result["contact_detail"]['country'] = data['country']
#         result["contact_detail"]['email'] = data['email']
        
#         result["supportive_document"]['manufacturer_logo_url'] = manufacturer_logo_url
#         result["supportive_document"]['bank_passbook'] =bank_passbook
#         id=CombineTable(**result).save()
#         return {"status":"success","message":"Data updated Successfully!"}
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
#         return { 'status': "error","message" :str(e)}


# @router.get('/')
# def get_single_data(data:str):
#     ids=http_operation.get_single_data(data,CombineTable)
#     return ids


# @router.delete("/api/delete/data")
# def delete_data(data:str):
#     response=http_operation.delete_data(data,CombineTable)
#     return response
    
# @router.get("/get/all/data")
# def get_all_db():
#     # dbname='tis_ecommerce_service'
#     # tabelname='combine_table'
#     data=http_operation.get_data_all()
#     result =db.post_demo.aggregate([{
#        '$lookup' : {'from': 'comment_demo','localField': 'title','foreignField': 'posttitle','as': 'comments' }
#     },{'$project':{'_id':1,'title':1,'post_id':1}},{'$out':'info'}])
#     for i in result:
#         print("i",i)
#     return data
    
# @router.post('/create/data')
# def create_data(data:int,name:str,username=Depends(auth_handler.auth_wrapper)):
#     dict1={'name':name,'data':data}
#     # print()
#     data= http_operation.insert_data(dict1,TestTabel,username,Demo)
#     return {"status":"success","message":"Data added Successfully!"}

# @router.put('/update/data')
# def update_data(id:str,data:int,name:str):
#         dict1={'id':id,'data':data,'name':name}
#         data1= http_operation.update_data(dict1,TestTabel)
#         return data1

#     # querydata=db.collection.aggregate([{"$group" : {"_id" : "$city"}}])    may i know this query is correct or not


# @router.post('/create/data/post')
# def postdemo(title:str,author:str,like:int,username=Depends(auth_handler.auth_wrapper)):
#     get_data = Rider.objects(username=username)
#     get_data = get_data.to_json()
#     userdata = json.loads(get_data)
#     post_id = userdata[0]['_id']['$oid']
#     print(post_id)
 
#     dict1={'title':title,'author':author,'like':like,'post_id':post_id}
#     id=post_demo(**dict1).save()
#     result =db.post_demo.aggregate([{
#        '$lookup' : {'from': 'comment_demo','localField': 'title','foreignField': 'posttitle','as': 'comments' }
#     }])
#     for i in result:
#         print("i",i)
#     # df=post_demo.aggregate([{ '$lookup':{'from': "comment_demo",'localField': "title",'foreignField': "posttitle",'as': "comments"}}]).to_mongo()
   
#     # print(df)
#     return {'status':"added!"}


# @router.post('/create/data/comment')
# def comment_demoo(posttitle:str,comment:str,like:int):
#     dict1={'posttitle':posttitle,'comment':comment,'like':like}
#     id=comment_demo(**dict1).save()

@router.post('/db/test')
def fun(rating: Optional[int] = None):
    username=Depends(auth_handler.auth_wrapper)
    get_data=Store.objects(username=username)
    # print("get_data",get_data)
    # get_data = get_data.to_json()
    # print("get_data",get_data)
    # userdata = json.loads(get_data)
    # print("get_data",userdata)
    # username1=userdata[0]['_id']
    # dict2={'user_profile':userdata}
    # print("get_data",username1)
    # print("username",dict2)

    return {'data':'rating','username':"asdfv"}

#  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjcwODA2OTksImlhdCI6MTY2Njk2NDI5OSwic3ViIjoibXVza2FuIn0.nrVknof6Uuiy3JC9NiwIlzXvB1KRMV2QJhr6RyJqqOs
