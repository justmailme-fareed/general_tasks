"""
FileName : common_notification.py
Description : This file manage user files upload.
Author : Tree Integrated services
Created Date : 18-01-2022
"""

from fastapi import APIRouter,Depends,Response,status
from fastapi.exceptions import HTTPException
import logging
import boto3
from configuration.config import ACCESS_KEY_ID,SECRET_ACCESS_KEY,IMAGE_QUALITY
import logging
from botocore.exceptions import ClientError,NoCredentialsError,EndpointConnectionError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase



###################################################### AWS Connection Details ########################################################
aws_region="ap-south-1"
def connect_aws_service(service_type):
    try:
        sns_client = boto3.client(service_type,aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY,region_name=aws_region)
        return sns_client
    except NoCredentialsError:
        return { 'status': "error","message" :"Invalid Credentials"}

def subscribe_sns_notifications(topic_name, protocol, endpoint):
    """
    :param topic: The topic to subscribe to.
    :param protocol: The protocol of the endpoint, such as 'sms' or 'email'.
    :param endpoint: The endpoint that receives messages, such as a phone number
                     (in E.164 format) for SMS messages, or an email address for
                     email messages.
    :return: The newly added subscription.
    """
    sns_client = connect_aws_service('sns') 
    try:
        topic_details = sns_client.create_topic(Name=topic_name)
        subscription = sns_client.subscribe(TopicArn=topic_details['TopicArn'], Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
        return subscription
    except ClientError:
        return { 'status': "error","message" :f"Couldn't subscribe to topic {topic_name}"}


###################################################### AWS SES Mailing section ########################################################
def send_sns_mail_notification(mailing_details, attachments: list=None):
    sender='fareed.fd7@gmail.com'
    recipients=mailing_details['from_recipients']
    cc=mailing_details['cc_recipients']
    bcc=mailing_details['bcc_recipients']
    title=mailing_details['title']
    text=mailing_details['text']
    body=mailing_details['body']
    
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
        

        message['To'] = ', '.join(recipients)
        message['CC'] = ', '.join(cc)
        message['BCC'] = ', '.join(bcc)

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

        
        destinations.extend(recipients)
        destinations.extend(cc)
        destinations.extend(bcc)
        ses_response = ses_client.send_raw_email(Source=sender, Destinations=destinations, RawMessage={'Data': message.as_string()})
    except ClientError as e:
        return { 'status': "error","message" :e.response['Error']['Message']}
    else:
        #data=["message_id": ses_response['MessageId']]
        return { 'status': "success","message" :'mail sent successfully'}


def send_sns_mail_notification1(to_email,from_email):
    
    # server = smtplib.SMTP("email-smtp.ap-south-1.amazonaws.com",587)
    # server.starttls()
    # #server.login("canamotorcar@gmail.com","rbsqpnozcaynslhw")
    # #server.sendmail("canamotorcar@gmail.com","mohammedfareed@treeis.in","f test mail")
    # server.login("AKIA4FMTAOBO4MVVLTBB","BGRxJW9kyGb+geTT2My3XjqHQ2FTUyJdHH/xRjoimlQn")
    # server.sendmail("sampath@treeis.in","fareed.fd7@gmail.com","f test mail")
    
    # raise SystemExit('dd')
    
    
    ses_client = connect_aws_service('ses')
    to_mail_list = ['mohammedfareed@treeis.in','vpsampath95@gmail.com','sampath@treeis.in',]
    email_body_text = "ses test email from aws"        
    # The character encoding for the email.
    email_charset = "UTF-8"
    email_msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    email_msg['Subject'] = "subject"
    email_msg['From'] = "mohammedfareed@treeis.in"
    email_msg['To'] = to_mail_list
    # email_msg['Cc'] = ', '.join(email Cc list)
    # email_msg['Bcc'] = ', '.join(email bcc list)
    email_msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(email_body_text.encode(email_charset), 'plain', email_charset)
    #htmlpart = MIMEText(email_body_html.encode(email_charset), 'html', email_charset)
    # Add the text and HTML parts to the child container.
    email_msg_body.attach(textpart)
    #email_msg_body.attach(htmlpart)
    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.mohammedfareed@treeis.in
    try:
        # Provide the contents of the email.
        # response = ses_client.send_raw_email(Source='sampath@treeis.in',Destinations=to_mail_list,RawMessage={'Data': email_msg.as_string()})
        # raise SystemExit('d')
        response = ses_client.send_email(
        Destination={'ToAddresses': to_mail_list},
        Message={
            'Body': {
                'Text': {
                    'Charset': "UTF-8",
                    'Data': 'SES test mail body',
                },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': 'SES test mail subject',
            },
        },
        Source='fareed.fd7@gmail.com',
    )
        raise SystemExit(response)
            # Display an error if something goes wrong.
    except ClientError as e:
            raise SystemExit(e.response['Error']['Message'])
    except EndpointConnectionError as exp:
            raise SystemExit(exp)
    except ConnectionError as exp:
           raise SystemExit(exp)
    except:
                print("Unknown Exception(AWS SES) while sending Email")