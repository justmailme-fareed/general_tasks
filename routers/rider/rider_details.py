import logging,os,json
from typing import List
from fastapi import  APIRouter,Depends,Response,status,Form,UploadFile,File,Request,Body
from pydantic import EmailStr
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
from typing import Optional,Union
from routers.rider.rider_schema import rider,Gender,Blood_group,Jobtype,User_type
from common.validation import form_validation
from routers.rider import strong_password
from database.connection import *
from datetime import date,datetime
from bson import ObjectId
cwd=os.getcwd()

from collections import Counter
from common.http_operation import get_record_count,get_records,get_record
from common.file_upload import validate_and_upload_image_s3,validate_and_delete_image_s3
from bson.json_util import loads
from bson.json_util import dumps

#strong password 
#password=strong_password.password
   
router = APIRouter(
    prefix=api_version + "/store",
    tags=["Rider"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()

#s3_bucket_name="tis-ftest"
s3_bucket_name="tis-store-admin"
s3_region="ap-south-1"
s3_bucket_dir="rider/"


#create rider
@router.post('/rider',status_code=201)
async def create_rider(response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date,None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : int = Form(),aadhar_number : int = Form(),pan_number: str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Form(...),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(unique=True),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(...),ifsc_code : str = Form(),user_type : User_type = Form(),user_data=Depends(auth_handler.auth_wrapper),rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    try: 
        firstname=form_validation.form_name_validate(firstname,3,30,'First name')
        lastname=form_validation.form_name_validate(lastname,1,30,'Last name')
        street_name=form_validation.form_name_validate(street_name,3,30,'Street name')
        area=form_validation.form_name_validate(area,3,30,'Area')
        state=form_validation.form_name_validate(state,2,30,'State')
        city=form_validation.form_name_validate(city,3,30,'City')

        pincode=form_validation.form_pin_validate(pincode,'Pincode')
        aadhar_number=form_validation.form_aadhar_validation(aadhar_number)
        pan_number=form_validation.form_pan_number_validation(pan_number)

        bank_name=form_validation.form_name_validate(bank_name,3,30,'Bank name')
        branch_name=form_validation.form_name_validate(branch_name,3,30,'Branch name')
        account_number=form_validation.form_acc_validate(account_number,'Account no')

        phone=form_validation.form_mobile_validate(phone,'Phone number')
        if alternate_phone:
            alternate_phone=form_validation.form_mobile_validate(alternate_phone,'Alternate Phone number')
        driving_license_number=form_validation.form_drivinglicense_validation(driving_license_number)
        ifsc_code=form_validation.form_ifsc_code_validation(ifsc_code)

        language_arr=language_known[0].split(',')
        for lang in language_arr:
            lang=form_validation.form_name_validate(lang,3,30,'Language')

        duplicate_lang_list = Counter(language_arr)
        for value,count in duplicate_lang_list.items():
            if count > 1:
                response.status_code = status.HTTP_409_CONFLICT
                return {'status': "error", "message" :f"Duplicate languages name {value}"}
        
        name_record_count = get_record_count(db.rider,{"store_id":ObjectId(user_data['id']),"status":"A","personal_detail.firstname":firstname})
        if name_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider name {firstname} already exists"}
        mobile_record_count = get_record_count(db.rider,{"store_id":ObjectId(user_data['id']),"status":"A","contact_detail.phone":phone})
        if mobile_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider mobile number {phone} already exists"}
        email_record_count = get_record_count(db.rider,{"store_id":ObjectId(user_data['id']),"status":"A","contact_detail.email":email})
        if email_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider email {email} already exists"}
        adhar_record_count = get_record_count(db.rider,{"store_id":ObjectId(user_data['id']),"status":"A","personal_detail.aadhar_number":aadhar_number})
        if adhar_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider aadhar number {aadhar_number} already exists"}
        
        store_rec_count = get_record_count(db.rider,{"store_id":ObjectId(user_data['id'])})
        emp_no='-00'+ str(store_rec_count+1)
        if len(str(store_rec_count))==2:
            emp_no='-0'+ str(store_rec_count+1)
        if len(str(store_rec_count))==3:
            emp_no='-'+str(store_rec_count+1)
        employee_id="R"+ city[:3] + emp_no
        # password=auth_handler.get_password_hash(strong_password.password)
        password=auth_handler.get_password_hash("rider@123")  

        rider_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,rider_image_url,s3_bucket_dir+'profile/')
        if rider_upload_result['status']=='error':
            return rider_upload_result
        rider_image_path=rider_upload_result['uploaded_file_url']

        aadhar_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,aadhar_image_url,s3_bucket_dir+'aadhar/')
        if aadhar_upload_result['status']=='error':
            return aadhar_upload_result
        aadhar_image_path=aadhar_upload_result['uploaded_file_url']
  
        driv_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,driving_license_url,s3_bucket_dir+'driving_license/')
        if driv_upload_result['status']=='error':
            return driv_upload_result
        driv_image_path=driv_upload_result['uploaded_file_url']

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
                         "language_known":language_arr,
                         "door_number":door_number,
                         "street_name":street_name,
                         "area":area,
                         "city":city,
                         "state":state,
                         "pincode":pincode,
                         "aadhar_number":aadhar_number,
                         "pan_number":pan_number,
                         "job_type":job_type
                        }

        driving_license_detail={"driving_license_number":driving_license_number,"expiry_date":str(driving_license_expiry_date)}
        bank_detail={"bank_name":bank_name, "branch_name":branch_name,"account_number":account_number,"ifsc_code":ifsc_code,}
        contact_detail={"phone":phone,"alternate_phone":alternate_phone,"email":email}
        supportive_document={"rider_image_url":rider_image_path,"aadhar_image_url":aadhar_image_path,"driving_license_url":driv_image_path,"bank_passbook_url":bankp_image_path}
        
        raide_details={"personal_detail":personal_detail,
                        "driving_license_detail":driving_license_detail,
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
        #raise SystemExit(raide_details)
        rider(**raide_details).save()
        return {'status': "success", "message" :f"Rider {firstname} added successfully","employee_id":employee_id}

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
        

#Get singel rider data
@router.get('/rider/{id}',status_code=200)
def rider_single_data(id : str,response : Response,user=Depends(auth_handler.auth_wrapper)):
    try:
        id= form_validation.form_objectID_validate(id,'Rider ID')
        if rider.objects.filter(id=id,status="A",store_id=user['id']):
            get_data = rider.objects.get(id=id,status="A",store_id=user['id'])
            get_data = get_data.to_json()
            data = json.loads(get_data)
            record={"id":data['_id']['$oid'],"personal_detail":data['personal_detail'],"contact_detail":data['contact_detail'],"bank_detail":data['bank_detail'],
            "supportive_document":data['supportive_document'],"driving_license_detail":data['driving_license_detail'],
            "user_type":data['user_type'],"status":data['status'],"employee_id":data['employee_id']}
            return { 'status': "success","data": record}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No record found for given rider ID {id}"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
 
# get rider all data
@router.get("/rider")
def rider_all_data(response:Response,name:Optional[str] = "",skip:int=0,limit:int=25,user=Depends(auth_handler.auth_wrapper)):
    try:
        status_code = status.HTTP_200_OK
        error_result= { 'status': "success","message" :"No records found","data":[]}
        where_condtion={"status" :'A',"store_id":ObjectId(user['id'])}
        if name:
            name= form_validation.form_name_validate(name,1,50,'Rider name')
            where_condtion={'personal_detail.firstname': { '$regex': name},"status" :'A',"store_id":ObjectId(user['id'])}
            status_code = status.HTTP_404_NOT_FOUND
            error_result= { 'status': "error","message" :f"No records found for given name {name}"}
        record_count = get_record_count(db.rider,where_condtion)
        if record_count == 0:
            response.status_code = status_code
            return error_result
        get_data = get_records(db.rider,where_condtion,skip,limit)
        data=loads(dumps(get_data))
        records=[]
        for rec in data:
            records.append({"id":str(rec['_id']),"personal_detail":rec['personal_detail'],"contact_detail":rec['contact_detail'],"bank_detail":rec['bank_detail'],
            "supportive_document":rec['supportive_document'],"driving_license_detail":rec['driving_license_detail'],
            "user_type":rec['user_type'],"status":rec['status'],"employee_id":rec['employee_id']})
        return {'status': "success","count":record_count,"data": records}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
    
#Delete Rider Data
@router.delete('/rider/{id}')
def delete_rider(id : str, response : Response,user=Depends(auth_handler.auth_wrapper)):
    try:
        id= form_validation.form_objectID_validate(id,'Rider ID')
        if rider.objects.filter(id=id,status="A",store_id=user['id']):
            get_data = rider.objects.get(id=id,status="A",store_id=user['id'])
            get_data = get_data.to_json()
            data = json.loads(get_data)
            name=data['personal_detail']['firstname']
            rider_doc_list=data['supportive_document']
            rider_doc_url_list=[rider_doc_list['rider_image_url'],rider_doc_list['aadhar_image_url'],rider_doc_list['driving_license_url'],rider_doc_list['bank_passbook_url']]
            rider_details={
                        "status":'D',
                        "updated_at":datetime.now(),
                        "updated_by":user['id'],
                        }
            rider.objects(id=id).update(**rider_details)
           # rider.objects(id=id).delete()
            # for image in rider_doc_url_list:
            #     image_url=image.split(s3_bucket_dir)
            #     image_file_location= s3_bucket_dir+image_url[1]
            #     validate_and_delete_image_s3(s3_bucket_name,image_file_location)
            return {'status': "success", "message": f"Rider {name} deleted successfully"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No record found for given Rider ID {id}"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error", "message": str(e)}


#Update rider
@router.put('/rider/{id}',status_code=200)
async def update_rider_details(id:str,response : Response,request: Request,firstname : str = Form(),lastname : str = Form(),dob :  Union[date,None] = Form(...),blood_group:Blood_group=Form(),gender :  Gender = Form(),language_known : List[str] = Form(),door_number : int = Form(),street_name : str = Form(),area : str = Form(),city : str = Form(),state : str = Form(),pincode : int = Form(),aadhar_number : int = Form(),pan_number: str = Form(),driving_license_number : str = Form(),driving_license_expiry_date : Union[date, None] = Form(...),job_type : Jobtype = Form(),phone : str = Form(),alternate_phone:Optional[str]=Form(None),email : EmailStr = Form(unique=True),bank_name : str = Form(),branch_name : str = Form(),account_number : int = Form(...),ifsc_code : str = Form(),user_type : User_type = Form(),user_data=Depends(auth_handler.auth_wrapper),rider_image_url:UploadFile = File(...),aadhar_image_url:UploadFile = File(...),driving_license_url:UploadFile = File(...),bank_passbook_url:UploadFile = File(...)):
    try:
        id= form_validation.form_objectID_validate(id,'Rider ID')   
        firstname=form_validation.form_name_validate(firstname,3,30,'First name')
        lastname=form_validation.form_name_validate(lastname,1,30,'Last name')
        street_name=form_validation.form_name_validate(street_name,3,30,'Street name')
        area=form_validation.form_name_validate(area,3,30,'Area')
        state=form_validation.form_name_validate(state,2,30,'State')
        city=form_validation.form_name_validate(city,3,30,'City')

        pincode=form_validation.form_pin_validate(pincode,'Pincode')
        aadhar_number=form_validation.form_aadhar_validation(aadhar_number)
        pan_number=form_validation.form_pan_number_validation(pan_number)

        bank_name=form_validation.form_name_validate(bank_name,3,30,'Bank name')
        branch_name=form_validation.form_name_validate(branch_name,3,30,'Branch name')
        account_number=form_validation.form_acc_validate(account_number,'Account no')
        phone=form_validation.form_mobile_validate(phone,'Phone number')
        if alternate_phone:
            alternate_phone=form_validation.form_mobile_validate(alternate_phone,'Alternate Phone number')
        driving_license_number=form_validation.form_drivinglicense_validation(driving_license_number)
        ifsc_code=form_validation.form_ifsc_code_validation(ifsc_code)
        record_data = get_record(db.rider,{"_id":ObjectId(id),"status":"A","store_id":ObjectId(user_data['id'])})
        if not record_data:
            response.status_code = status.HTTP_404_NOT_FOUND
            return { 'status': "error","message" :f"No record found for given rider ID {id}"}
        record_count = get_record_count(db.rider,{"_id" : {"$ne" : ObjectId(id)},"status":"A","personal_detail.firstname":firstname,"store_id":ObjectId(user_data['id'])})
        if record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider name {firstname} already exists"}
        mobile_record_count = get_record_count(db.rider, {"_id" : {"$ne" : ObjectId(id)},"status":"A","contact_detail.phone":phone,"store_id":ObjectId(user_data['id'])})
        if mobile_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider mobile number {phone} already exists"}
        email_record_count = get_record_count(db.rider, {"_id" : {"$ne" : ObjectId(id)},"status":"A","contact_detail.email":email,"store_id":ObjectId(user_data['id'])})
        if email_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider email {email} already exists"}
        adhar_record_count = get_record_count(db.rider, {"_id" : {"$ne" : ObjectId(id)},"status":"A","personal_detail.aadhar_number":firstname,"store_id":ObjectId(user_data['id'])})
        if adhar_record_count > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return {'status': "error", "message" :f"Rider aadhar number {aadhar_number} already exists"}
    
        language_arr=language_known[0].split(',')
        for lang in language_arr:
            lang=form_validation.form_name_validate(lang,1,50,'Language')

        duplicate_lang_list = Counter(language_arr)
        for value,count in duplicate_lang_list.items():
            if count > 1:
                response.status_code = status.HTTP_409_CONFLICT
                return {'status': "error", "message" :f"Duplicate languages name {value}"}
        
        rider_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,rider_image_url,s3_bucket_dir+'profile/')
        if rider_upload_result['status']=='error':
            return rider_upload_result
        rider_image_path=rider_upload_result['uploaded_file_url']

        aadhar_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,aadhar_image_url,s3_bucket_dir+'aadhar/')
        if aadhar_upload_result['status']=='error':
            return aadhar_upload_result
        aadhar_image_path=aadhar_upload_result['uploaded_file_url']
  
        driv_upload_result = await validate_and_upload_image_s3(response,s3_bucket_name,driving_license_url,s3_bucket_dir+'driving_license/')
        if driv_upload_result['status']=='error':
            return driv_upload_result
        driv_image_path=driv_upload_result['uploaded_file_url']

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
                         "language_known":language_arr,
                         "door_number":door_number,
                         "street_name":street_name,
                         "area":area,
                         "city":city,
                         "state":state,
                         "pincode":pincode,
                         "aadhar_number":aadhar_number,
                          "pan_number":pan_number,
                          "job_type":job_type,
                        }
        
        driving_license_detail={"driving_license_number":driving_license_number,"expiry_date":str(driving_license_expiry_date)}
        bank_detail={"bank_name":bank_name, "branch_name":branch_name,"account_number":account_number,"ifsc_code":ifsc_code,}
        contact_detail={"phone":phone,"alternate_phone":alternate_phone,"email":email}
        supportive_document={"rider_image_url":rider_image_path,"aadhar_image_url":aadhar_image_path,"driving_license_url":driv_image_path,"bank_passbook_url":bankp_image_path}
        
        rider_details={"personal_detail":personal_detail,
                        "driving_license_detail":driving_license_detail,
                        "bank_detail":bank_detail,
                        "contact_detail":contact_detail,
                        "supportive_document":supportive_document,
                        "user_type":user_type,
                        "updated_at":datetime.now(),
                        "updated_by":user_data['id'],
                        }
        rider.objects(id=id).update(**rider_details)
        rider_doc_list=record_data['supportive_document']
        rider_doc_url_list=[rider_doc_list['rider_image_url'],rider_doc_list['aadhar_image_url'],rider_doc_list['driving_license_url'],rider_doc_list['bank_passbook_url']]
        for image in rider_doc_url_list:
            image_url=image.split(s3_bucket_dir)
            image_file_location= s3_bucket_dir+image_url[1]
            validate_and_delete_image_s3(s3_bucket_name,image_file_location)
        return {'status': "success", "message" :f"Rider details updated successfully"}

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}
   