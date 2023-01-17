from mongoengine import *
from enum import Enum
from datetime import datetime
from bson.objectid import ObjectId

#Gender Enum Values
class Gender(str,Enum):
    male="male"
    female="female"
    others="others"

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

#User type Enum Values
class User_type(str,Enum):
    rider='rider'
    # store='store'
    # user='user'

class store_status(str,Enum):
    A='A'
    I='I'
    B='B'
    D='D'
    L='L'



#Jobtype Enum Values
class Jobtype(str,Enum):
    fulltime='fulltime'
    partime='partime'
    contract='contract'

class PersonalDetails(EmbeddedDocument):
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    dob = StringField(required=True)
    blood_group = EnumField(Blood_group,required=True)
    gender = EnumField(Gender,required=True)
    language_known=ListField(required=True)
    door_number=IntField(required=True)
    street_name=StringField(required=True)
    area=StringField(required=True)
    city=StringField(required=True)
    state=StringField(required=True)
    pincode=IntField(required=True)
    aadhar_number=IntField(required=True)
    pan_number=StringField(required=True)
    job_type = EnumField(Jobtype, default=Jobtype.fulltime,required=True)
    

class BankDetail(EmbeddedDocument):
    bank_name = StringField(required=True)
    branch_name = StringField(required=True)
    account_number=IntField(required=True)
    ifsc_code=StringField(required=True)
  
class ContactDetail(EmbeddedDocument):
    phone=StringField(required=True)
    alternate_phone=StringField()
    email=EmailField(required=True)#unique=True

class DrivingDetail(EmbeddedDocument):
    driving_license_number=StringField(required=True)
    expiry_date =StringField(required=True)
   
class SupportiveDocument(EmbeddedDocument):
    rider_image_url = StringField()
    aadhar_image_url = StringField()
    driving_license_url = StringField()
    bank_passbook_url = StringField()

class rider(Document):
    personal_detail = EmbeddedDocumentField(PersonalDetails)
    bank_detail = EmbeddedDocumentField(BankDetail)
    contact_detail=EmbeddedDocumentField(ContactDetail)
    supportive_document = EmbeddedDocumentField(SupportiveDocument)
    driving_license_detail = EmbeddedDocumentField(DrivingDetail)
    user_type=StringField(required=True)
    status=EnumField(store_status, default=store_status.A,required=True)
    password=StringField(requird=True)
    store_id=ObjectIdField()
    employee_id=StringField(requird=True)
    created_by=ObjectIdField(requird=True)
    updated_by=ObjectIdField(requird=True)
    created_at=DateTimeField(required=True,default=datetime.now())
    updated_at=DateTimeField(required=True,default=datetime.now())

    