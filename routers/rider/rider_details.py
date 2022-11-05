import logging,os,json,uuid
from typing import List
from fastapi import  APIRouter,Depends,Response,status,Form,UploadFile,File,Request,Body
from pydantic import EmailStr
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
from typing import Optional,Union
from routers.rider.rider_schema import Rider
from common.validation import validation
from routers.rider import strong_password
from database import connection
from pathlib import Path
import numpy as np
from enum import Enum
from datetime import date,datetime

#strong password 
password=strong_password.password

#Gender Enum Values
class Gender(str,Enum):
    male="male"
    female="female"
    others="others"

#User type Enum Values
class User_type(str,Enum):
    rider='rider'
    # store='store'
    # user='user'

#Store status Enum Values
class store_status(str,Enum):
    A='A'
    I='I'
    B='B'
    D='D'
    L='L'

#Blood group Enum Values
class Blood_group(str,Enum):
    A='A+'
    a='A-'
    B='B+'
    b='B-'
    AB='AB+'
    ab='AB-'
    O='O+'
    o='O-'

#Jobtype Enum Values
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

#create rider
@router.post('/rider',status_code=201)
async def create_rider(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date,None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : str = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),status : store_status = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Form(...),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(max_length=11,min_length=11),ifsc_code : str = Form(),user_type : User_type = Form(),user_data=Depends(auth_handler.auth_wrapper),rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    try:
        data = await request.form()
        data = dict(data)
        emp_id=[]
        user_id=user_data['id']
        firstname=validation.name_validation(firstname,'First Name',3,30)
        lastname=validation.name_validation(lastname,'Last Name',3,30)
        street_name=validation.name_validation(street_name,'Street name',3,30)
        area=validation.name_validation(area,'Area',3,30)
        state=validation.name_validation(state,'State',3,30)
        city=validation.name_validation(city,'City',3,30)
        pincode=validation.pincode_validation(pincode)
        aadhar_number=validation.aadhar_validation(aadhar_number)
        bank_name=validation.name_validation(bank_name,'Bank Name',3,30)
        branch_name=validation.name_validation(branch_name,'Branch name',3,30)
        phone=validation.mobile_validate(phone,'True','Phone Number')
        alternate_phone=validation.mobile_validate(alternate_phone,'False','Alternate Phone Number')
        driving_license_number=validation.drivinglicense_validation(driving_license_number)
        ifsc_code=validation.ifsc_code_validation(ifsc_code)
        language_known=np.array(str(language_known[0]).split(','))
        # return language_known
        if city:
            emp_city=city[:3]
        if data['user_type'] =="rider":
            emp_id.append('R')
        elif data['user_type'] =="store_user":
            emp_id.append('S')
        collection_count=connection.collection['rider'].count_documents({})
        employee_id=str(emp_id[0]) + emp_city + '-00'+ str(collection_count+1)

        # Rider Image URL upload process
        if rider_image_url:
            rider_image_url_path = "uploads/rider/profile/"
            rider_image_extension = rider_image_url.filename.split(".")[-1]
            rider_image_url.filename = f"{uuid.uuid4()}.{rider_image_extension}"
            contents = await rider_image_url.read()
            if not os.path.exists(f"{rider_image_url_path}{rider_image_url.filename}"):
                create_path=Path(rider_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{rider_image_url_path}{rider_image_url.filename}", "wb") as f:
                f.write(contents)
    
        # Aadhar Image URL upload process
        if aadhar_image_url:
            aadhar_image_url_path = "uploads/rider/aadhar/"
            aadhar_image_extension = aadhar_image_url.filename.split(".")[-1]
            aadhar_image_url.filename = f"{uuid.uuid4()}.{aadhar_image_extension}"
            contents = await aadhar_image_url.read()
            if not os.path.exists(f"{aadhar_image_url_path}{aadhar_image_url.filename}"):
                create_aadhar_image_path=Path(aadhar_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{aadhar_image_url_path}{aadhar_image_url.filename}", "wb") as f:
                f.write(contents)

        # Driving Licesne Image URL upload process
        if driving_license_url:
            driving_license_image_url_path = "uploads/rider/driving_license/"
            driving_license_image_extension = driving_license_url.filename.split(".")[-1]
            driving_license_url.filename = f"{uuid.uuid4()}.{driving_license_image_extension}"
            contents = await driving_license_url.read()
            if not os.path.exists(f"{driving_license_image_url_path}{driving_license_url.filename}"):
                create_path=Path(driving_license_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{driving_license_image_url_path}{driving_license_url.filename}", "wb") as f:
                f.write(contents)

        # Bank Passbook  Image URL upload process
        if bank_passbook_url:
            bank_passbook_image_path = "uploads/rider/bank_passbook/"
            bank_passbook_image_extension = bank_passbook_url.filename.split(".")[-1]
            bank_passbook_url.filename = f"{uuid.uuid4()}.{bank_passbook_image_extension}"
            contents = await bank_passbook_url.read()
            if not os.path.exists(f"{bank_passbook_image_path}{bank_passbook_url.filename}"):
                create_path=Path(bank_passbook_image_path).mkdir(parents=True, exist_ok=True)
            with open(f"{bank_passbook_image_path}{bank_passbook_url.filename}", "wb") as f:
                f.write(contents)
        
        result = {}
        # Rider Personal Details
        result["personal_detail"] = {}
        result["personal_detail"]["firstname"] = data['firstname']
        result["personal_detail"]["lastname"] = data['lastname']
        result["personal_detail"]["dob"] = data['dob']
        result["personal_detail"]["blood_group"] = data['blood_group']
        result["personal_detail"]["gender"] = data['gender']
        result["personal_detail"]["language_known"] =language_known.tolist()
        result["personal_detail"]['door_number'] = data['door_number']
        result["personal_detail"]['street_name'] = data['street_name']
        result["personal_detail"]['area'] = data['area']
        result["personal_detail"]['city'] = data['city']
        result["personal_detail"]['state'] = data['state']
        result["personal_detail"]['pincode'] = int(data['pincode'])
        result["personal_detail"]['aadhar_number'] = data['aadhar_number']
        
        # Rider Driving License Details
        result["driving_license_detail"] = {}
        result["driving_license_detail"]['driving_license_number'] = data['driving_license_number']
        result["driving_license_detail"]['driving_license_expiry_date'] = data['driving_license_expiry_date']
        
        # Rider Bank Details
        result["bank_detail"] = {}
        result["bank_detail"]['bank_name'] = data['bank_name']
        result["bank_detail"]['branch_name'] = data['branch_name']
        result["bank_detail"]['account_number'] = int(data['account_number'])
        result["bank_detail"]['ifsc_code'] = data['ifsc_code']
        
        # Rider Contact Details
        result['contact_detail']={}
        result["contact_detail"]['phone'] = data['phone']
        result["contact_detail"]['alternate_phone'] = alternate_phone
        result["contact_detail"]['job_type'] = data['job_type']
        result["contact_detail"]['email'] = data['email']
        
        # Rider Images
        result['supportive_document']={}
        result["supportive_document"]['rider_image_url'] = f"{rider_image_url_path}{rider_image_url.filename}"
        result["supportive_document"]['aadhar_image_url'] =f"{aadhar_image_url_path}{aadhar_image_url.filename}"
        result["supportive_document"]['driving_license_url'] =f"{driving_license_image_url_path}{driving_license_url.filename}"
        result["supportive_document"]['bank_passbook_url'] =f"{bank_passbook_image_path}{bank_passbook_url.filename}"
        
        # Rider Employee Details
        result['user_type']= user_type
        result['status'] =data['status']
        result['password'] = password
        result['created_at'],result['updated_at'] = datetime.now(),datetime.now()
        result['created_by'],result['updated_by'],result['store_id'] = user_id,user_id,user_id
        result['employee_id'] = employee_id
        Rider(**result).save()
        return {"status":"success","message":f"Rider added Successfully!"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}


#Get singel rider data
@router.get('/rider/{id}',status_code=200)
def rider_single_data(id : str,response : Response,username=Depends(auth_handler.auth_wrapper)):
    try:
        id = id.strip()
        get_data = Rider.objects(id= id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': "error","message" :f"Rider not exist for this id"}
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        del userdata[0]["_id"]
        return {'status': "success","data" :userdata}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
 
# get rider all data
@router.get("/rider")
def rider_all_data(response:Response,skip: int = 0, limit: int = 25,username=Depends(auth_handler.auth_wrapper)):
    try:
        if limit>1:
            rider_collection = connection.collection["rider"]
            if rider_collection.count_documents({})<1:
                return {"status":"sucess","data":[],'message':"No rider data found"}
            data=[]
            for collection in rider_collection.find({}).limit(limit).skip(skip):
                collection["_id"] = str(collection["_id"])
                data.append(collection)
            return {"status":"success","data":data,'count':rider_collection.count_documents({})}
        else:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {"status":"error","message":"Please enter valid rider limit!"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

#Delete Rider Data
@router.delete('/rider/{id}')
def delete_rider(id : str, response : Response,username=Depends(auth_handler.auth_wrapper)):
    try:
        id = id.strip()
        get_data = Rider.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': "error","message" :f"Rider not exist for this id"}
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        rider_fullname=f"{userdata[0]['personal_detail']['firstname']} {userdata[0]['personal_detail']['lastname']}"
        rider_image_url=userdata[0]['supportive_document']
        for image_url,rider_value in rider_image_url.items():
            os.remove(rider_value)
        Rider.objects(id = id).delete()
        return {'status': "success","message" :f"Rider {rider_fullname} deleted successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

# Rider Update Data
@router.put('/rider/{id}',status_code=200)
async def rider_update(id:str,response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Form(...),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone : str = Form(),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : str = Form(),ifsc_code : str = Form(),user_type : User_type = Form(),status : store_status = Form(),rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...),user_data=Depends(auth_handler.auth_wrapper)):
    try:
        id = id.strip()
        get_data = Rider.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': "error","message" :f"Rider not exist for this id"}
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        user_id = userdata[0]["_id"]
        rider_image_url=userdata[0]['supportive_document']
        for image_url,rider_value in rider_image_url.items():
            os.remove(rider_value)
        Rider.objects(id = id).delete()
        data = await request.form()
        data = dict(data)
        emp_id=[]
        user_id=user_data['id']
        
        firstname=validation.name_validation(firstname,'first_name',3,30)
        lastname=validation.name_validation(lastname,'last_name',3,30)
        street_name=validation.name_validation(street_name,'street_name',3,30)
        area=validation.name_validation(area,'area',3,30)
        city=validation.name_validation(city,'city',3,30)
        state=validation.name_validation(state,'state',3,30)
        pincode=validation.pincode_validation(pincode)
        aadhar_number=validation.aadhar_validation(aadhar_number)
        driving_license_number=validation.drivinglicense_validation(driving_license_number)
        phone=validation.mobile_validate(phone,'True','phone number')
        alternate_phone=validation.mobile_validate(alternate_phone,'False','alternate phone number')
        bank_name=validation.name_validation(bank_name,'bank_name',3,30)
        branch_name=validation.name_validation(branch_name,'branch_name',3,30)
        ifsc_code=validation.ifsc_code_validation(ifsc_code)
        if city:
            emp_city=city[:3]
        if data['user_type'] =="rider":
            emp_id.append('R')
        elif data['user_type'] =="store_user":
            emp_id.append('S')
        collection_count=connection.collection['rider'].count_documents({})
        employee_id=str(emp_id[0]) + emp_city + '-00'+ str(collection_count+1)

        # Rider Image URL upload process
        if rider_image_url:
            rider_image_url_path = "uploads/rider/profile/"
            rider_image_extension = rider_image_url.filename.split(".")[-1]
            rider_image_url.filename = f"{uuid.uuid4()}.{rider_image_extension}"
            contents = await rider_image_url.read()
            if not os.path.exists(f"{rider_image_url_path}{rider_image_url.filename}"):
                create_path=Path(rider_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{rider_image_url_path}{rider_image_url.filename}", "wb") as f:
                f.write(contents)
    
        # Aadhar Image URL upload process
        if aadhar_image_url:
            aadhar_image_url_path = "uploads/rider/aadhar/"
            aadhar_image_extension = aadhar_image_url.filename.split(".")[-1]
            aadhar_image_url.filename = f"{uuid.uuid4()}.{aadhar_image_extension}"
            contents = await aadhar_image_url.read()
            if not os.path.exists(f"{aadhar_image_url_path}{aadhar_image_url.filename}"):
                create_aadhar_image_path=Path(aadhar_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{aadhar_image_url_path}{aadhar_image_url.filename}", "wb") as f:
                f.write(contents)

        # Driving Licesne Image URL upload process
        if driving_license_url:
            driving_license_image_url_path = "uploads/rider/driving_license/"
            driving_license_image_extension = driving_license_url.filename.split(".")[-1]
            driving_license_url.filename = f"{uuid.uuid4()}.{driving_license_image_extension}"
            contents = await driving_license_url.read()
            if not os.path.exists(f"{driving_license_image_url_path}{driving_license_url.filename}"):
                create_path=Path(driving_license_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{driving_license_image_url_path}{driving_license_url.filename}", "wb") as f:
                f.write(contents)

        # Bank Passbook  Image URL upload process
        if bank_passbook_url:
            bank_passbook_image_path = "uploads/rider/bank_passbook/"
            bank_passbook_image_extension = bank_passbook_url.filename.split(".")[-1]
            bank_passbook_url.filename = f"{uuid.uuid4()}.{bank_passbook_image_extension}"
            contents = await bank_passbook_url.read()
            if not os.path.exists(f"{bank_passbook_image_path}{bank_passbook_url.filename}"):
                create_path=Path(bank_passbook_image_path).mkdir(parents=True, exist_ok=True)
            with open(f"{bank_passbook_image_path}{bank_passbook_url.filename}", "wb") as f:
                f.write(contents)
        
        result = {}
        # Rider Personal Details
        result["personal_detail"] = {}
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
        
        # Rider Driving License Details
        result["driving_license_detail"] = {}
        result["driving_license_detail"]['driving_license_number'] = data['driving_license_number']
        result["driving_license_detail"]['driving_license_expiry_date'] = data['driving_license_expiry_date']
        
        # Rider Bank Details
        result["bank_detail"] = {}
        result["bank_detail"]['bank_name'] = data['bank_name']
        result["bank_detail"]['branch_name'] = data['branch_name']
        result["bank_detail"]['account_number'] = data['account_number']
        result["bank_detail"]['ifsc_code'] = data['ifsc_code']
        
        # Rider Contact Details
        result['contact_detail']={}
        result["contact_detail"]['phone'] = data['phone']
        result["contact_detail"]['alternate_phone'] = alternate_phone
        result["contact_detail"]['job_type'] = data['job_type']
        result["contact_detail"]['email'] = data['email']
        
        # Rider Images
        result['supportive_document']={}
        result["supportive_document"]['rider_image_url'] = f"{rider_image_url_path}{rider_image_url.filename}"
        result["supportive_document"]['aadhar_image_url'] =f"{aadhar_image_url_path}{aadhar_image_url.filename}"
        result["supportive_document"]['driving_license_url'] =f"{driving_license_image_url_path}{driving_license_url.filename}"
        result["supportive_document"]['bank_passbook_url'] =f"{bank_passbook_image_path}{bank_passbook_url.filename}"
        
        # Rider Employee Details
        result["employee_detail"]={}
        result["employee_detail"]['user_type'] = data['user_type']
        result["employee_detail"]['status'] = data['status']
        result["employee_detail"]['password'] = password
        result["employee_detail"]['created_at'],result["employee_detail"]['updated_at'] = datetime.now(),datetime.now()
        result["employee_detail"]['created_by'],result["employee_detail"]['updated_by'],result["employee_detail"]['store_id'] = user_id,user_id,user_id
        result["employee_detail"]['employee_id'] = employee_id
        Rider(**result).save()
        return {"status":"success","message":f"Rider updated Successfully!"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
 
