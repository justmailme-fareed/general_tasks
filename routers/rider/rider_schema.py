from mongoengine import *
from enum import Enum
from datetime import datetime
from bson.objectid import ObjectId

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

class storeDetails(Document):
    firstname = StringField(required=True,min_length=3,max_length=20)
    lastname = StringField(required=True,min_length=3,max_length=20)
    dob = StringField(required=True)
    bloodgroup = EnumField(Blood_group,required=True)
    gender = EnumField(Gender,required=True)
    language_known=ListField(required=True)
    door_number=IntField(required=True)
    street_name=StringField(required=True)
    area=StringField(required=True)
    city=StringField(required=True)
    state=StringField(required=True)
    pincode=IntField(required=True)
    aadhar_number=IntField(required=True)

class BankDetail(Document):
    bank_name = StringField(required=True,min_length=3,max_length=30)
    branch_name = StringField(required=True,min_length=3,max_length=50)
    account_number=StringField(required=True)
    ifsc_code=StringField(required=True)
  
class ContactDetail(Document):
    phone=StringField(required=True,min_length=10,max_length=10)
    alternate_phone=StringField(required=True,min_length=10,max_length=10)
    job_type = EnumField(Jobtype, default=Jobtype.fulltime,required=True)
    email=EmailField(required=True)

class DrivingDetail(Document):
    driving_license_number=StringField(required=True)
    phodriving_license_expiry_datene=StringField(required=True)
   
class SupportiveDocument(Document):
    rider_image_url = StringField()
    aadhar_image_url = StringField()
    driving_license_url = StringField()
    bank_passbook_url = StringField()

class Rider(Document):
    personal_detail = ReferenceField(storeDetails)
    bank_detail = ReferenceField(BankDetail)
    contact_detail=ReferenceField(ContactDetail)
    supportive_document = ReferenceField(SupportiveDocument)
    driving_license_detail = ReferenceField(DrivingDetail)
    user_type=EnumField(User_type, default=User_type.rider,required=True)
    status=EnumField(store_status, default=store_status.A,required=True)
    password=StringField(requird=True)
    store_id=ObjectIdField(requird=True)
    employee_id=ObjectIdField(requird=True)
    created_by=ObjectIdField(requird=True)
    updated_by=ObjectIdField(requird=True)
    created_at=DateTimeField(required=True,default=datetime.now())
    updated_at=DateTimeField(required=True,default=datetime.now())

    