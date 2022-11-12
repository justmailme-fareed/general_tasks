import logging,json,pymongo,os
from fastapi import  APIRouter,Depends,Response,status,Form,UploadFile,File,Request,Body
from pydantic import EmailStr
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
from typing import Optional,Union
import uuid
from routers.store_user.store_schema import Store_Employee
from common.validation import validation
from routers.rider import strong_password
from datetime import date,datetime
from enum import Enum
from database import connection
from pathlib import Path

#strong password 
password=strong_password.password


#Gender Enum Values
class Gender(str,Enum):
    male="male"
    female="female"
    others="others"

#User type Enum Values  
class User_type(str,Enum):
    store='store_employee'

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
    tags=["Store User"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()

#create store employee 
@router.post('/employee',status_code=201)
async def create_store_employee(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(...),ifsc_code : str = Form(),user_type : User_type = Form(),user_data=Depends(auth_handler.auth_wrapper),user_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
        data = await request.form()
        data = dict(data)
        emp_id=[]
        user_id=user_data['id']
        firstname=validation.name_validation(firstname,'First Name',3,30)
        lastname=validation.name_validation(lastname,'Last Name',3,30)
        street_name=validation.name_validation(street_name,'Street Name',3,30)
        area=validation.name_validation(area,'Area',3,30)
        city=validation.name_validation(city,'City',3,30)
        state=validation.name_validation(state,'State',3,30)
        pincode=validation.pincode_validation(pincode)
        aadhar_number=validation.aadhar_validation(aadhar_number)
        phone=validation.mobile_validate(phone,'True','Phone Number')
        alternate_phone=validation.mobile_validate(alternate_phone,'False','Alternate Phone Number')
        bank_name=validation.name_validation(bank_name,'Bank Name',3,30)
        branch_name=validation.name_validation(branch_name,'Branch Name',3,30)
        account_number=validation.account_number_validation(account_number)
        ifsc_code=validation.ifsc_code_validation(ifsc_code)
    
        # User Image URL upload process
        if user_image_url:
            user_image_url_path = "uploads/store_user/user_image/"
            user_image_url_extension = user_image_url.filename.split(".")[-1]
            user_image_url.filename = f"{uuid.uuid4()}.{user_image_url_extension}"
            contents = await user_image_url.read()
            if not os.path.exists(f"{user_image_url_path}{user_image_url.filename}"):
                create_path=Path(user_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{user_image_url_path}{user_image_url.filename}", "wb") as f:
                f.write(contents)
    
        # Aadhar Image URL upload process
        if aadhar_image_url:
            aadhar_image_url_path = "uploads/store_user/user_image"
            aadhar_image_extension = aadhar_image_url.filename.split(".")[-1]
            aadhar_image_url.filename = f"{uuid.uuid4()}.{aadhar_image_extension}"
            contents = await aadhar_image_url.read()
            if not os.path.exists(f"{aadhar_image_url_path}{aadhar_image_url.filename}"):
                create_aadhar_image_path=Path(aadhar_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{aadhar_image_url_path}{aadhar_image_url.filename}", "wb") as f:
                f.write(contents)

        # Bank Passbook  Image URL upload process
        if bank_passbook_url:
            bank_passbook_image_path = "uploads/store_user/bank_passbook"
            bank_passbook_image_extension = bank_passbook_url.filename.split(".")[-1]
            bank_passbook_url.filename = f"{uuid.uuid4()}.{bank_passbook_image_extension}"
            contents = await bank_passbook_url.read()
            if not os.path.exists(f"{bank_passbook_image_path}{bank_passbook_url.filename}"):
                create_path=Path(bank_passbook_image_path).mkdir(parents=True, exist_ok=True)
            with open(f"{bank_passbook_image_path}{bank_passbook_url.filename}", "wb") as f:
                f.write(contents)
        
        #generate employe_id 
        if city:
            emp_city=city[:3]
        if user_type:
            emp_id.append('S')
        collection_count=connection.collection['store__employee'].count_documents({})
        employee_id=str(emp_id[0]) + emp_city + '-00'+ str(collection_count+1)
       
        result = {}
        # Store Employee Personal Details
        result["personal_detail"] = {}
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
        result["personal_detail"]['pincode'] = int(data['pincode'])
        result["personal_detail"]['aadhar_number'] = data['aadhar_number']
    
        # Store Employee Bank Details
        result["bank_detail"] = {}
        result["bank_detail"]['bank_name'] = data['bank_name']
        result["bank_detail"]['branch_name'] = data['branch_name']
        result["bank_detail"]['account_number'] = int(data['account_number'])
        result["bank_detail"]['ifsc_code'] = data['ifsc_code']
        
        # Store Employee Contact Details
        result['contact_detail']={}
        result["contact_detail"]['phone'] = data['phone']
        result["contact_detail"]['alternate_phone'] = alternate_phone
        result["contact_detail"]['email'] = data['email']
        
        # Store Employee Images 
        result['supportive_document']={}
        result["supportive_document"]['user_image_url'] = f"{user_image_url_path}{user_image_url.filename}"
        result["supportive_document"]['aadhar_image_url'] =f"{aadhar_image_url_path}{aadhar_image_url.filename}"
        result["supportive_document"]['bank_passbook_url'] =f"{bank_passbook_image_path}{bank_passbook_url.filename}"
        
        # Store Employee Details
        result['user_type'] = user_type
        result['password'] = password
        result['created_at'],result['updated_at'] = datetime.now(),datetime.now()
        result['created_by'],result['updated_by'],result['store_id'] = user_id,user_id,user_id
        result['employee_id'] = employee_id   
        Store_Employee(**result).save()
        return {"status":"success","message":f"Store Employee added Successfully!"}
    

# get single store employee data
@router.get('/employee/{id}',status_code=200)
def store_employee_single_data(id : str,response : Response,user_data=Depends(auth_handler.auth_wrapper)):
    try:
        get_data = Store_Employee.objects(id= id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': "error","message" :f"Store Employee not exist for this id"}
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        del userdata[0]["_id"]
        return {'status': "success","data" :userdata}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
 
# get all store employee data
@router.get("/employee")
def store_employee_all_data(response:Response,skip: int = 0, limit: int = 25,user_data=Depends(auth_handler.auth_wrapper)):
        collections = connection.collection["store__employee"]
        if limit >0:
            if collections.count_documents({})<1:
                return {"status":"sucess","data":[],'message':"No rider data found"}
            elif limit > collections.count_documents({}):
                response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                return {"status":"error","message":"You are finding out of limit Store Employees!"}
            data=[]
            for store_collection in collections.find({}).limit(limit).skip(skip):
                store_collection["_id"] = str(store_collection["_id"])
                store_collection["store_id"] = str(store_collection["store_id"])
                store_collection["created_by"] = str(store_collection["created_by"])
                store_collection["updated_by"] = str(store_collection["updated_by"])
                data.append(store_collection)
            return {"status":"success","data":data,'count':collections.count_documents({})}
        else:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {"status":"error","message":"You are finding out of limit Store mployees!"}
    
# Delete store employee data
@router.delete('/employee/{id}')
def delete_store_employee(id : str, response : Response,user_data=Depends(auth_handler.auth_wrapper)):
    try:
        get_data = Store_Employee.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': "error","message" :f"Store employee not exist for this id"}
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        user_id = userdata[0]["_id"]
        rider_image_url=userdata[0]['supportive_document']
        store_employee_fullname=f"{userdata[0]['personal_detail']['firstname']} {userdata[0]['personal_detail']['lastname']}"
        for image_url,value in rider_image_url.items():
            os.remove(value)
        Store_Employee.objects(id = id).delete()
        return {'status': "success","message" :f"Store employee {store_employee_fullname} deleted Successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

#update store employee data
@router.put('/employee/{id}')
async def  store_employee_update(id:str,response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : str = Form(),aadhar_number : str = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(...),ifsc_code : str = Form(),user_type : User_type = Form(),user_data=Depends(auth_handler.auth_wrapper),user_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)): 
        get_data = Store_Employee.objects(id=id)
        if not get_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'status': "error","message" :f"Store employee not exist for this id"}
        get_data = get_data.to_json()
        userdata = json.loads(get_data)
        user_id = userdata[0]["_id"]
        data = await request.form()
        data = dict(data)
        emp_id=[]
        user_id=user_data['id']
        
        firstname=validation.name_validation(firstname,'First Name',3,30)
        lastname=validation.name_validation(lastname,'Last Name',3,30)
        street_name=validation.name_validation(street_name,'Street Name',3,30)
        area=validation.name_validation(area,'Area',3,30)
        city=validation.name_validation(city,'City',3,30)
        state=validation.name_validation(state,'State',3,30)
        pincode=validation.pincode_validation(pincode)
        aadhar_number=validation.aadhar_validation(aadhar_number)
        phone=validation.mobile_validate(phone,'True','Phone Number')
        alternate_phone=validation.mobile_validate(alternate_phone,'False','Alternate Phone Number')
        bank_name=validation.name_validation(bank_name,'Bank Name',3,30)
        branch_name=validation.name_validation(branch_name,'Branch Name',3,30)
        account_number=validation.account_number_validation(account_number)
        ifsc_code=validation.ifsc_code_validation(ifsc_code)
    
        # User Image URL upload process
        if user_image_url:
            user_image_url_path = "uploads/store_user/user_image/"
            user_image_url_extension = user_image_url.filename.split(".")[-1]
            user_image_url.filename = f"{uuid.uuid4()}.{user_image_url_extension}"
            contents = await user_image_url.read()
            if not os.path.exists(f"{user_image_url_path}{user_image_url.filename}"):
                create_path=Path(user_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{user_image_url_path}{user_image_url.filename}", "wb") as f:
                f.write(contents)
    
        # Aadhar Image URL upload process
        if aadhar_image_url:
            aadhar_image_url_path = "uploads/store_user/user_image"
            aadhar_image_extension = aadhar_image_url.filename.split(".")[-1]
            aadhar_image_url.filename = f"{uuid.uuid4()}.{aadhar_image_extension}"
            contents = await aadhar_image_url.read()
            if not os.path.exists(f"{aadhar_image_url_path}{aadhar_image_url.filename}"):
                create_aadhar_image_path=Path(aadhar_image_url_path).mkdir(parents=True, exist_ok=True)
            with open(f"{aadhar_image_url_path}{aadhar_image_url.filename}", "wb") as f:
                f.write(contents)

        # Bank Passbook  Image URL upload process
        if bank_passbook_url:
            bank_passbook_image_path = "uploads/store_user/bank_passbook"
            bank_passbook_image_extension = bank_passbook_url.filename.split(".")[-1]
            bank_passbook_url.filename = f"{uuid.uuid4()}.{bank_passbook_image_extension}"
            contents = await bank_passbook_url.read()
            if not os.path.exists(f"{bank_passbook_image_path}{bank_passbook_url.filename}"):
                create_path=Path(bank_passbook_image_path).mkdir(parents=True, exist_ok=True)
            with open(f"{bank_passbook_image_path}{bank_passbook_url.filename}", "wb") as f:
                f.write(contents)
        
        #generate employe_id 
        if city:
            emp_city=city[:3]
        if user_type:
            emp_id.append('S')
        collection_count=connection.collection['store__employee'].count_documents({})
        employee_id=str(emp_id[0]) + emp_city + '-00'+ str(collection_count+1)

        result = {}
        # Store Employee Personal Details
        result["personal_detail"] = {}
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
        result["personal_detail"]['pincode'] = (data['pincode'])
        result["personal_detail"]['aadhar_number'] = data['aadhar_number']
    
        # Store Employee Bank Details
        result["bank_detail"] = {}
        result["bank_detail"]['bank_name'] = data['bank_name']
        result["bank_detail"]['branch_name'] = data['branch_name']
        result["bank_detail"]['account_number'] = data['account_number']
        result["bank_detail"]['ifsc_code'] = data['ifsc_code']
        
        # Store Employee Contact Details
        result['contact_detail']={}
        result["contact_detail"]['phone'] = data['phone']
        result["contact_detail"]['alternate_phone'] = alternate_phone
        result["contact_detail"]['email'] = data['email']
        
        # Store Employee Images 
        result['supportive_document']={}
        result["supportive_document"]['user_image_url'] = f"{user_image_url_path}{user_image_url.filename}"
        result["supportive_document"]['aadhar_image_url'] =f"{aadhar_image_url_path}{aadhar_image_url.filename}"
        result["supportive_document"]['bank_passbook_url'] =f"{bank_passbook_image_path}{bank_passbook_url.filename}"
        
        # Store Employee Details
        result['user_type'] = user_type
        result['password'] = password
        result['created_by'],result['updated_by'],result['store_id'] = user_id,user_id,user_id
        result['employee_id'] = employee_id
        rider_image_url=userdata[0]['supportive_document']
        for image_url,value in rider_image_url.items():
            os.remove(value)
        Store_Employee.objects(id = id).delete()
        Store_Employee(**result).save()
        return {"status":"success","message":f"Store Employee Updated Successfully!"}
