import logging,json
from fastapi import  APIRouter,Depends,Response,Request,status,Form,UploadFile,File
from configuration.config import api_version
from routers.user.user_auth import AuthHandler
from typing import Optional,Union,List
from common.validation import form_validation
from database.connection import *
from datetime import date,datetime
from common.notification.message import *
from common.notification.common_notification import send_ses_mail_notification,create_ses_mail_template,update_ses_mail_template,delete_ses_mail_template,send_ses_mail_notification_with_template
from common.file_upload import validate_and_upload_email_template_image_s3

router = APIRouter(
    prefix=api_version + "/notification",
    tags=["Notification"],
    responses={404: {"description": "Not found"}},
)
auth_handler = AuthHandler()

s3_bucket_name="tis-ui"
s3_region="ap-south-1"
s3_template_image_dir="notifications/email/"

@router.post('/send-mail',status_code=200)
def send_mail_notification(response : Response,request: Request,attachment:Optional[UploadFile] = File(None)):
    try:
        mailing_details={
            'to_recipients':['sampath@treeis.in'],
            'cc_recipients':['mohammedfareed@treeis.in'],
            'bcc_recipients':[],
            'no_reply_email':['fareed.fd7@gmail.com']
        }
        template_details={
            'template_name':'Welcome',
            'template_data':'{ \"name\":\"sampath\" }'
        }
        result=send_ses_mail_notification_with_template(mailing_details,template_details,attachment)
        if result['status']=='error':
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

@router.post('/create-template',status_code=201)
def create_mail_template(response : Response,request: Request,template_name : str = Form(),template_subject : str = Form(),template_file_name : str = Form()):
    try:
        result=create_ses_mail_template(template_name,template_subject,template_file_name)
        if result['status']=='error':
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

@router.delete('/delete-template',status_code=200)
def delete_mail_template(response : Response,request: Request,template_name : str = Form()):
    try:
        result=delete_ses_mail_template(template_name)
        if result['status']=='error':
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}

@router.put('/update-template',status_code=200)
def update_mail_template(response : Response,request: Request,template_name : str = Form(),template_subject : str = Form(),template_file_name : str = Form()):
    try:
        result=update_ses_mail_template(template_name,template_subject,template_file_name)
        if result['status']=='error':
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {'status': "error","message" :str(e)}


#Product Image Data
@router.post('/upload-template-image', status_code=201)
async def upload_template_image(response : Response,template_name : str = Form(),template_image_url: List[UploadFile] = File(...)):
    try:
        other_image_url=[]
        for p_image in template_image_url:
            if p_image is not None:
                validate_image = await validate_and_upload_email_template_image_s3(response,s3_bucket_name,p_image,s3_template_image_dir+template_name+'/')
                if validate_image['status']=='error':
                    return validate_image
                other_location=validate_image['uploaded_file_url']
                other_image_url.append(other_location) 
        data={"template_name":template_name,"template_image":other_image_url}
        return {'status': "success", "message" :"Template image uploaded successfully" ,"data":data}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

