from fileinput import filename
import logging,os,json,pymongo
import re
from typing import List
from fastapi import  APIRouter,Depends,Response,status,Form,UploadFile,File,Request,Body
from pydantic import EmailStr
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
from typing import Optional,Union
from routers.rider.rider_schema import Rider, images
from common.validation import validation
from routers.rider import strong_password
from datetime import date,datetime
from pathlib import Path
from enum import Enum

current_dir=str(Path.cwd())
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
password=strong_password.password
mongoURI = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongoURI)
db = client["tis_ecommerce_service"]

 
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

router = APIRouter(
    prefix=api_version + "/store",
    tags=["Rider"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()

@router.post('/rider',status_code=201)
async def create_rider(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Body(default="2022-06-13"),
blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Body(default="2022-06-13"),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(),ifsc_code : str = Form(),user_type : User_type = Form(),store_status : store_status = Form(),user_data=Depends(auth_handler.auth_wrapper)
,rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    data = await request.form()
    collection = db["rider"]
    data = dict(data)
    emp_id=[]
    userdata=user_data['id']
    if rider_image_url:
        rider_image_video = f"./uploads/rider/profile"
        if not os.path.exists(rider_image_video):
                create_path=Path(f"{current_dir}/uploads/rider/profile").mkdir(parents=True, exist_ok=True)
                create_rider_location = f"./uploads/rider/profile/{current_time}_{rider_image_url.filename}"
                split_tup = os.path.splitext(create_rider_location)
                with open(create_rider_location, "wb+") as file_object:
                    file_object.write(aadhar_image_url.file.read())
                    print("in1")
                rider_image_url=create_rider_location
        else:
            rider_image_video=f'./uploads/rider/profile/{current_time}_{rider_image_url.filename}'
            split_tup = os.path.splitext(rider_image_video)
            with open(rider_image_video, "wb+") as file_object:
                file_object.write(rider_image_url.file.read())
                print("in2")
            rider_image_url=rider_image_video
    if aadhar_image_url:
        aadhar_location = f"./uploads/rider/aadhar"
        if not os.path.exists(aadhar_location):
            create_path=Path(f"{current_dir}/uploads/rider/aadhar").mkdir(parents=True, exist_ok=True)
            aadhar_location = f"./uploads/rider/aadhar/{current_time}_{aadhar_image_url.filename}"
            split_tup = os.path.splitext(aadhar_location)
            with open(aadhar_location, "wb+") as file_object:
                file_object.write(aadhar_image_url.file.read())
                print("in1")
                aadhar_image_url=aadhar_location
        else:
            aadhar_location=f'./uploads/rider/aadhar/{current_time}_{aadhar_image_url.filename}'
            split_tup = os.path.splitext(aadhar_location)
            with open(aadhar_location, "wb+") as file_object:
                file_object.write(aadhar_image_url.file.read())
                print("in2")
            aadhar_image_url=aadhar_location
    if driving_license_url:
        driving_license_location = f"./uploads/rider/driving_license"
        if not os.path.exists(driving_license_location):
            create_path=Path(f"{current_dir}/uploads/rider/driving_license").mkdir(parents=True, exist_ok=True)
            driving_license_location = f"./uploads/rider/driving_license/{current_time}_{driving_license_url.filename}"
            split_tup = os.path.splitext(driving_license_location)
            with open(driving_license_location, "wb+") as file_object:
                file_object.write(driving_license_url.file.read())
                print("in1")
                driving_license_url=driving_license_location
        else:
            driving_license_location=f'./uploads/rider/driving_license/{current_time}_{driving_license_url.filename}'
            split_tup = os.path.splitext(driving_license_location)
            with open(driving_license_location, "wb+") as file_object:
                file_object.write(driving_license_url.file.read())
                print("in2")
            driving_license_url=driving_license_location    
    
    if bank_passbook_url:
        bank_passbook_location = f"./uploads/rider/bank_passbook"
        if not os.path.exists(bank_passbook_location):
            create_path=Path(f"{current_dir}/uploads/rider/bank_passbook").mkdir(parents=True, exist_ok=True)
            bank_passbook_location = f"./uploads/rider/bank_passbook/{current_time}_{bank_passbook_url.filename}"
            split_tup = os.path.splitext(bank_passbook_location)
            with open(bank_passbook_location, "wb+") as file_object:
                file_object.write(bank_passbook_url.file.read())
                bank_passbook_url=bank_passbook_location
        else:
            bank_passbook_location=f'./uploads/rider/bank_passbook/{current_time}_{bank_passbook_url.filename}'
            split_tup = os.path.splitext(bank_passbook_location)
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
    collection_count=collection.count_documents({})
    employee_id=str(emp_id[0]) + emp_city + '-00'+ str(collection_count+1)


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
@router.get('/rider/{id}',status_code=200)
def rider_single_data(id : str,response : Response,username=Depends(auth_handler.auth_wrapper)):
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
 
@router.get("/rider")
def rider_all_data(username=Depends(auth_handler.auth_wrapper)):
    rider_collection = db["rider"]

    response = rider_collection.find({})
    data=[]
    for collection in response:
        collection["_id"] = str(collection["_id"])
        data.append(collection)
    return {"status":"success","data":data}

#Delete User Data
@router.delete('/rider/{id}',status_code=200)
def delete_rider(id : str, response : Response,username=Depends(auth_handler.auth_wrapper)):
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

@router.put('/rider/{id}')
async def store_update(id:str,response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Body(default="2022-06-13"),blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Body(default="2022-06-13"),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone : str = Form(),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(),ifsc_code : str = Form(),user_type : User_type = Form(),store_status : store_status = Form(),rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...),username=Depends(auth_handler.auth_wrapper)):
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
            rider_image_video = f"./uploads/rider/profile"
            if not os.path.exists(rider_image_video):
                    create_path=Path(f"{current_dir}/uploads/rider/profile").mkdir(parents=True, exist_ok=True)
                    create_rider_location = f"./uploads/rider/profile/{current_time}_{rider_image_url.filename}"
                    split_tup = os.path.splitext(create_rider_location)
                    with open(create_rider_location, "wb+") as file_object:
                        file_object.write(aadhar_image_url.file.read())
                        print("in1")
                    rider_image_url=create_rider_location
            else:
                rider_image_video=f'./uploads/rider/profile/{current_time}_{rider_image_url.filename}'
                split_tup = os.path.splitext(rider_image_video)
                with open(rider_image_video, "wb+") as file_object:
                    file_object.write(rider_image_url.file.read())
                    print("in2")
                rider_image_url=rider_image_video
        if aadhar_image_url:
            aadhar_location = f"./uploads/rider/aadhar"
            if not os.path.exists(aadhar_location):
                create_path=Path(f"{current_dir}/uploads/rider/aadhar").mkdir(parents=True, exist_ok=True)
                aadhar_location = f"./uploads/rider/aadhar/{current_time}_{aadhar_image_url.filename}"
                split_tup = os.path.splitext(aadhar_location)
                with open(aadhar_location, "wb+") as file_object:
                    file_object.write(aadhar_image_url.file.read())
                    print("in1")
                    aadhar_image_url=aadhar_location
            else:
                aadhar_location=f'./uploads/rider/aadhar/{current_time}_{aadhar_image_url.filename}'
                split_tup = os.path.splitext(aadhar_location)
                with open(aadhar_location, "wb+") as file_object:
                    file_object.write(aadhar_image_url.file.read())
                    print("in2")
                aadhar_image_url=aadhar_location
        if driving_license_url:
            driving_license_location = f"./uploads/rider/driving_license"
            if not os.path.exists(driving_license_location):
                create_path=Path(f"{current_dir}/uploads/rider/driving_license").mkdir(parents=True, exist_ok=True)
                driving_license_location = f"./uploads/rider/driving_license/{current_time}_{driving_license_url.filename}"
                split_tup = os.path.splitext(driving_license_location)
                with open(driving_license_location, "wb+") as file_object:
                    file_object.write(driving_license_url.file.read())
                    print("in1")
                    driving_license_url=driving_license_location
            else:
                driving_license_location=f'./uploads/rider/driving_license/{current_time}_{driving_license_url.filename}'
                split_tup = os.path.splitext(driving_license_location)
                with open(driving_license_location, "wb+") as file_object:
                    file_object.write(driving_license_url.file.read())
                    print("in2")
                driving_license_url=driving_license_location    
    
        if bank_passbook_url:
            bank_passbook_location = f"./uploads/rider/bank_passbook"
            if not os.path.exists(bank_passbook_location):
                create_path=Path(f"{current_dir}/uploads/rider/bank_passbook").mkdir(parents=True, exist_ok=True)
                bank_passbook_location = f"./uploads/rider/bank_passbook/{current_time}_{bank_passbook_url.filename}"
                split_tup = os.path.splitext(bank_passbook_location)
                with open(bank_passbook_location, "wb+") as file_object:
                    file_object.write(bank_passbook_url.file.read())
                    bank_passbook_url=bank_passbook_location
            else:
                bank_passbook_location=f'./uploads/rider/bank_passbook/{current_time}_{bank_passbook_url.filename}'
                split_tup = os.path.splitext(bank_passbook_location)
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
 