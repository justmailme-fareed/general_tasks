"""
FileName : common_notification.py
Description : This file manage user files upload.
Author : Tree Integrated services
Created Date : 18-01-2022
"""

from fastapi import APIRouter,Depends,Response,status
from fastapi.exceptions import HTTPException
import logging,os,json,pathlib
import boto3
from configuration.config import ACCESS_KEY_ID,SECRET_ACCESS_KEY,SES_MAIL_SENDER
import logging
from botocore.exceptions import ClientError,NoCredentialsError,EndpointConnectionError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase



###################################################### AWS Connection Details ########################################################
aws_region="ap-south-1"
template_dir="/templates/email_notification_template/"
def connect_aws_service(service_type):
    try:
        sns_client = boto3.client(service_type,aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name=aws_region)
        return sns_client
    except NoCredentialsError:
        return { 'status': "error","message" :"Invalid Credentials"}

def subscribe_sns_notifications(topic_name, protocol, endpoint):
   
    sns_client = connect_aws_service('sns') 
    try:
        topic_details = sns_client.create_topic(Name=topic_name)
        subscription = sns_client.subscribe(TopicArn=topic_details['TopicArn'], Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
        return subscription
    except ClientError:
        return { 'status': "error","message" :f"Couldn't subscribe to topic {topic_name}"}


###################################################### AWS SES Mailing Template section ########################################################
def create_ses_mail_template(template_name,template_subject,template_file_name):
    try:
        ses_client = connect_aws_service('ses')
        try:
            file_path=str(pathlib.Path().absolute())+template_dir+template_file_name
            with open(file_path, 'r') as f:
                template_html_part = f.read()
        except Exception as e:
            return {'status': "error","message" :str(e)}
        template_arr= {
                    "TemplateName": template_name,
                    "SubjectPart": template_subject,
                    "HtmlPart": template_html_part,
                    "TextPart": 'NA'
            }

        response = ses_client.create_template(Template = template_arr)
    except ClientError as e:
        return { 'status': "error","message" :e.response['Error']['Message']}
    else:
        return { 'status': "success","message" :'template created successfully'}


def delete_ses_mail_template(template_name):
    try:
        ses_client = connect_aws_service('ses')
        template_details = ses_client.get_template(TemplateName = template_name)
        if template_details:
            response = ses_client.delete_template(TemplateName = template_name)
    except ClientError as e:
        return { 'status': "error","message" :e.response['Error']['Message']}
    else:
        return { 'status': "success","message" :'template deleted successfully'}


def update_ses_mail_template(template_name,template_subject,template_file_name):
    try:
        ses_client = connect_aws_service('ses')
        try:
            file_path=str(pathlib.Path().absolute())+template_dir+template_file_name
            with open(file_path, 'r') as f:
                template_html_part = f.read()
        except Exception as e:
            return {'status': "error","message" :str(e)}
        
        template_details = ses_client.get_template(TemplateName = template_name)
        if template_details:
            template_arr= {
                        "TemplateName": template_name,
                        "SubjectPart": template_subject,
                        "HtmlPart": template_html_part,
                        "TextPart": 'NA'
                }

            response = ses_client.update_template(Template = template_arr)
    except ClientError as e:

        return { 'status': "error","message" :e.response['Error']['Message']}
    else:
        return { 'status': "success","message" :'template updated successfully'}

###################################################### AWS SES Mailing section ########################################################

def send_ses_mail_notification_with_template(mailing_details,template_details, attachments: list=None):
    to_recipients=mailing_details['to_recipients']
    cc_recipients=mailing_details['cc_recipients']
    bcc_recipients=mailing_details['bcc_recipients']
    no_reply_email=mailing_details['no_reply_email']

    template_name=template_details['template_name']
    template_data=template_details['template_data']
    #title='TIS SNS Test Mail'
    destinations = []
    try:
        ses_client = connect_aws_service('ses')
        ses_mail_response = ses_client.send_templated_email(
                    Source=SES_MAIL_SENDER,
                    Destination={
                        'ToAddresses': to_recipients,
                        'CcAddresses': cc_recipients,
                        'BccAddresses': bcc_recipients
                    },
                    ReplyToAddresses=no_reply_email,
                    Template=template_name,
                    TemplateData=template_data
                )
    except ClientError as e:
        return { 'status': "error","message" :e.response['Error']['Message']}
    else:
        #data=["message_id": ses_response['MessageId']]
        return { 'status': "success","message" :'mail sent successfully'}
   

def send_ses_mail_notification(mailing_details, attachments: list=None):
    sender='fareed.fd7@gmail.com'
    to_recipients=mailing_details['to_recipients']
    cc_recipients=mailing_details['cc_recipients']
    bcc_recipients=mailing_details['bcc_recipients']
    title=mailing_details['title']
    text=mailing_details['mail_text']
    body=mailing_details['mail_body']
    
    #title='TIS SNS Test Mail'
    destinations = []
    try:
        ses_client = connect_aws_service('ses')
        if text and body:
            # assign subtype - multipart/alternative
            content_subtype = 'alternative'
        else:
            # assign subtype - multipart/mixed
            content_subtype = 'mixed'

        # Instantiate a MIMEMultipart message object
        message = MIMEMultipart(content_subtype)
        message['Subject'] = title
        message['From'] = f"{sender}"
        message['To'] = ', '.join(to_recipients)
        message['CC'] = ', '.join(cc_recipients)
        message['BCC'] = ', '.join(bcc_recipients)

        # text - defined as text/plain part
        if text:
            part = MIMEText(text, 'plain')
            message.attach(part)
        # body - defined as text/html part
        if body:
            part = MIMEText(body, 'html')
            message.attach(part)

        # Add attachments
        for attachment in attachments or []:
            with open(attachment, 'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('Content-Disposition','attachment',filename=os.path.basename(attachment))
                message.attach(part)        
        destinations.extend(to_recipients)
        destinations.extend(cc_recipients)
        destinations.extend(bcc_recipients)
        ses_mail_response = ses_client.send_raw_email(Source=sender, Destinations=destinations, RawMessage={'Data': message.as_string()})
    except ClientError as e:
        return { 'status': "error","message" :e.response['Error']['Message']}
    else:
        #data=["message_id": ses_response['MessageId']]
        return { 'status': "success","message" :'mail sent successfully'}