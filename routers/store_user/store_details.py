import logging,json,os
from fastapi import  APIRouter,Depends,Response,status,Form,UploadFile,File,Request,Body
from pydantic import EmailStr
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
from typing import Optional,Union
from routers.store_user.store_schema import store_employee,Gender,Blood_group,User_type
from common.validation import form_validation
from routers.rider import strong_password
from datetime import date,datetime
from database.connection import *
from bson import ObjectId
from collections import Counter
from common.http_operation import get_record_count,get_records,get_record
from common.file_upload import validate_and_upload_image_s3,validate_and_delete_image_s3
from bson.json_util import loads
from bson.json_util import dumps

router = APIRouter(
    prefix=api_version + "/store",
    tags=["Store User"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()

cwd=os.getcwd()
#strong password 
password=strong_password.password

#s3_bucket_name="tis-ftest"
s3_bucket_name="tis-store-admin"
s3_region="ap-south-1"
s3_bucket_dir="store_employee/"

#create store employee 
@router.post('/employee',status_code=201)
async def create_store_employee(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date, None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : int = Form(),aadhar_number : int = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(...),ifsc_code : str = Form(),user_type : User_type = Form(),user_data=Depends(auth_handler.auth_wrapper),user_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    try:    
        firstname=form_validation.form_name_validate(firstname,3,30,'First name')
        lastname=form_validation.form_name_validate(lastname,3,30,'Last name')
        street_name=form_validation.form_name_validate(street_name,3,30,'Street name')
        area=form_validation.form_name_validate(area,3,30,'Area')
        state=form_validation.form_name_validate(state,2,30,'State')
        city=form_validation.form_name_validate(city,3,30,'City')

        pincode=form_validation.form_pin_acc_validate(pincode,6,'Pincode')
        aadhar_number=form_validation.form_aadhar_validation(aadhar_number)

        bank_name=form_validation.form_name_validate(bank_name,3,30,'Bank name')
        branch_name=form_validation.form_name_validate(branch_name,3,30,'Branch name')
        account_number=form_validation.form_pin_acc_validate(account_number,11,'Account no')
        ifsc_code=form_validation.form_ifsc_code_validation(ifsc_code)

        phone=form_validation.form_mobile_validate(phone,'Phone number')
        if alternate_phone:
            alternate_phone=form_validation.form_mobile_validate(alternate_phone,'Alternate Phone number')
        
        name_record_count = get_record_count(db.store_employee,{"store_id":ObjectId(user_data['id']),"status":"A","personal_detail.firstname":firstname})
        if name_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee name {firstname} already exists"}
        mobile_record_count = get_record_count(db.store_employee,{"store_id":ObjectId(user_data['id']),"status":"A","contact_detail.phone":phone})
        if mobile_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee mobile number {phone} already exists"}
        email_record_count = get_record_count(db.store_employee,{"store_id":ObjectId(user_data['id']),"status":"A","contact_detail.email":email})
        if email_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee email {email} already exists"}
        adhar_record_count = get_record_count(db.store_employee,{"store_id":ObjectId(user_data['id']),"status":"A","personal_detail.aadhar_number":aadhar_number})
        if adhar_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee aadhar number {aadhar_number} already exists"}
        
        store_rec_count = get_record_count(db.store_employee,{"store_id":ObjectId(user_data['id'])})
        emp_no='-00'+ str(store_rec_count+1)
        if len(str(store_rec_count))==2:
            emp_no='-0'+ str(store_rec_count+1)
        if len(str(store_rec_count))==3:
            emp_no='-'+str(store_rec_count+1)
        employee_id="S"+ city[:3] + emp_no

        user_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,user_image_url,s3_bucket_dir+'profile/')
        if user_upload_result['status']=='error':
            return user_upload_result
        user_image_path=user_upload_result['uploaded_file_url']

        aadhar_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,aadhar_image_url,s3_bucket_dir+'aadhar/')
        if aadhar_upload_result['status']=='error':
            return aadhar_upload_result
        aadhar_image_path=aadhar_upload_result['uploaded_file_url']

        bankp_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,bank_passbook_url,s3_bucket_dir+'bank_passbook/')
        if bankp_upload_result['status']=='error':
            return bankp_upload_result
        bankp_image_path=bankp_upload_result['uploaded_file_url']
        personal_detail={
                         "firstname":firstname,
                         "lastname":lastname,
                         "dob":str(dob),
                         "blood_group":blood_group,
                         "gender":gender,
                         "door_number":door_number,
                         "street_name":street_name,
                         "area":area,
                         "city":city,
                         "state":state,
                         "pincode":pincode,
                         "aadhar_number":aadhar_number,
                        }
        bank_detail={"bank_name":bank_name, "branch_name":branch_name,"account_number":account_number,"ifsc_code":ifsc_code,}
        contact_detail={"phone":phone,"alternate_phone":alternate_phone,"email":email}
        supportive_document={"user_image_url":user_image_path,"aadhar_image_url":aadhar_image_path,"bank_passbook_url":bankp_image_path}
        
        user_details={"personal_detail":personal_detail,
                        "bank_detail":bank_detail,
                        "contact_detail":contact_detail,
                        "supportive_document":supportive_document,
                        "user_type":user_type,
                        "employee_id": employee_id,
                        "password":password,
                        "store_id":user_data['id'],
                        "created_by":user_data['id'],
                        "updated_by":user_data['id'],
                        }
        store_employee(**user_details).save()
        return {'status': "success", "message" :f"Store employee {firstname} added successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
        
# get single store employee data
@router.get('/employee/{id}',status_code=200)
def store_employee_single_data(id : str,response : Response,user=Depends(auth_handler.auth_wrapper)):
    try:
        id= form_validation.form_objectID_validate(id,'Employee ID')
        if store_employee.objects.filter(id=id,status="A",store_id=user['id']):
            get_data = store_employee.objects.get(id=id,status="A",store_id=user['id'])
            get_data = get_data.to_json()
            data = json.loads(get_data)
            record={"id":data['_id']['$oid'],"personal_detail":data['personal_detail'],"contact_detail":data['contact_detail'],"bank_detail":data['bank_detail'],
            "supportive_document":data['supportive_document'],
            "user_type":data['user_type'],"status":data['status'],"employee_id":data['employee_id']}
            return { 'status': "success","data": record}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No record found for given store employee ID {id}"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
 
# get all store employee data
@router.get("/employee")
def store_employee_all_data(response:Response,name:Optional[str] = "",skip: int = 0, limit: int = 25,user=Depends(auth_handler.auth_wrapper)):
    try:
        status_code = status.HTTP_200_OK
        error_result= { 'status': "success","message" :"No records found","data":[]}
        where_condtion={"status" :'A',"store_id":ObjectId(user['id'])}
        if name:
            name= form_validation.form_name_validate(name,1,50,'Rider name')
            where_condtion={'personal_detail.firstname': { '$regex': name},"status" :'A',"store_id":ObjectId(user['id'])}
            status_code = status.HTTP_404_NOT_FOUND
            error_result= { 'status': "error","message" :f"No records found for given name {name}"}
        record_count = get_record_count(db.store_employee,where_condtion)
        if record_count == 0:
            response.status_code = status_code
            return error_result
        get_data = get_records(db.store_employee,where_condtion,skip,limit)
        data=loads(dumps(get_data))
        records=[]
        for rec in data:
            records.append({"id":str(rec['_id']),"personal_detail":rec['personal_detail'],"contact_detail":rec['contact_detail'],"bank_detail":rec['bank_detail'],
            "supportive_document":rec['supportive_document'],"user_type":rec['user_type'],"status":rec['status'],"employee_id":rec['employee_id']})
        return {'status': "success","count":record_count,"data": records}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
        
# Delete store employee data
@router.delete('/employee/{id}')
def delete_store_employee(id : str, response : Response,user=Depends(auth_handler.auth_wrapper)):
    try:
        id= form_validation.form_objectID_validate(id,'Employee ID')
        if store_employee.objects.filter(id=id,store_id=user['id']):
            get_data = store_employee.objects.get(id=id,store_id=user['id'])
            get_data = get_data.to_json()
            data = json.loads(get_data)
            name=data['personal_detail']['firstname']
            store_emp_doc_list=data['supportive_document']
            store_doc_url_list=[store_emp_doc_list['user_image_url'],store_emp_doc_list['aadhar_image_url'],store_emp_doc_list['bank_passbook_url']]
            rider_details={
                        "status":'D',
                        "updated_at":datetime.now(),
                        "updated_by":user['id'],
                        }
            store_employee.objects(id=id).update(**rider_details)
           # rider.objects(id=id).delete()
            # for image in store_doc_url_list:
            #     image_url=image.split(s3_bucket_dir)
            #     image_file_location= s3_bucket_dir+image_url[1]
            #     validate_and_delete_image_s3(s3_bucket_name,image_file_location)
            return {'status': "success", "message": f"Store employee {name} deleted successfully"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No record found for given Store employee ID {id}"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error", "message": str(e)} 


#Update store employee data
@router.put('/employee/{id}',status_code=200)
async def update_store_employee_details(id:str,response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date,None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : int = Form(),aadhar_number : int = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(unique=True),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(...),ifsc_code : str = Form(),user_type : User_type = Form(),user_data=Depends(auth_handler.auth_wrapper),user_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    try:
        id= form_validation.form_objectID_validate(id,'Rider ID')   
        firstname=form_validation.form_name_validate(firstname,3,30,'First name')
        lastname=form_validation.form_name_validate(lastname,3,30,'Last name')
        street_name=form_validation.form_name_validate(street_name,3,30,'Street name')
        area=form_validation.form_name_validate(area,3,30,'Area')
        state=form_validation.form_name_validate(state,2,30,'State')
        city=form_validation.form_name_validate(city,3,30,'City')

        pincode=form_validation.form_pin_acc_validate(pincode,6,'Pincode')
        aadhar_number=form_validation.form_aadhar_validation(aadhar_number)

        bank_name=form_validation.form_name_validate(bank_name,3,30,'Bank name')
        branch_name=form_validation.form_name_validate(branch_name,3,30,'Branch name')
        account_number=form_validation.form_pin_acc_validate(account_number,11,'Account no')
        ifsc_code=form_validation.form_ifsc_code_validation(ifsc_code)

        phone=form_validation.form_mobile_validate(phone,'Phone number')
        if alternate_phone:
            alternate_phone=form_validation.form_mobile_validate(alternate_phone,'Alternate Phone number')
        record_data = get_record(db.store_employee,{"_id":ObjectId(id),"status":"A","store_id":ObjectId(user_data['id'])})
        if not record_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No record found for given Store employee ID {id}"}
        record_count = get_record_count(db.store_employee,{"_id" : {"$ne" : ObjectId(id)},"status":"A","personal_detail.firstname":firstname,"store_id":ObjectId(user_data['id'])})
        if record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee name {firstname} already exists"}
        mobile_record_count = get_record_count(db.store_employee, {"_id" : {"$ne" : ObjectId(id)},"status":"A","contact_detail.phone":phone,"store_id":ObjectId(user_data['id'])})
        if mobile_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee mobile number {phone} already exists"}
        email_record_count = get_record_count(db.store_employee, {"_id" : {"$ne" : ObjectId(id)},"status":"A","contact_detail.email":email,"store_id":ObjectId(user_data['id'])})
        if email_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee email {email} already exists"}
        adhar_record_count = get_record_count(db.store_employee, {"_id" : {"$ne" : ObjectId(id)},"status":"A","personal_detail.aadhar_number":firstname,"store_id":ObjectId(user_data['id'])})
        if adhar_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Store employee aadhar number {aadhar_number} already exists"}
    
        user_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,user_image_url,s3_bucket_dir+'profile/')
        if user_upload_result['status']=='error':
            return user_upload_result
        user_image_path=user_upload_result['uploaded_file_url']

        aadhar_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,aadhar_image_url,s3_bucket_dir+'aadhar/')
        if aadhar_upload_result['status']=='error':
            return aadhar_upload_result
        aadhar_image_path=aadhar_upload_result['uploaded_file_url']

        bankp_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,bank_passbook_url,s3_bucket_dir+'bank_passbook/')
        if bankp_upload_result['status']=='error':
            return bankp_upload_result
        bankp_image_path=bankp_upload_result['uploaded_file_url']

        personal_detail={
                         "firstname":firstname,
                         "lastname":lastname,
                         "dob":str(dob),
                         "blood_group":blood_group,
                         "gender":gender,
                         "door_number":door_number,
                         "street_name":street_name,
                         "area":area,
                         "city":city,
                         "state":state,
                         "pincode":pincode,
                         "aadhar_number":aadhar_number,
                        }
        bank_detail={"bank_name":bank_name, "branch_name":branch_name,"account_number":account_number,"ifsc_code":ifsc_code,}
        contact_detail={"phone":phone,"alternate_phone":alternate_phone,"email":email}
        supportive_document={"user_image_url":user_image_path,"aadhar_image_url":aadhar_image_path,"bank_passbook_url":bankp_image_path}
        
        user_details={"personal_detail":personal_detail,
                        "bank_detail":bank_detail,
                        "contact_detail":contact_detail,
                        "supportive_document":supportive_document,
                        "user_type":user_type,
                        "password":password,
                        "store_id":user_data['id'],
                        "updated_at":datetime.now(),
                        "updated_by":user_data['id'],
                        }
        store_employee.objects(id=id).update(**user_details)
        store_emp_doc_list=record_data['supportive_document']
        store_doc_url_list=[store_emp_doc_list['user_image_url'],store_emp_doc_list['aadhar_image_url'],store_emp_doc_list['bank_passbook_url']]
        for image in store_doc_url_list:
            image_url=image.split(s3_bucket_dir)
            image_file_location= s3_bucket_dir+image_url[1]
            validate_and_delete_image_s3(s3_bucket_name,image_file_location)
        return {'status': "success", "message" :f"Store employee details updated successfully"}

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
   