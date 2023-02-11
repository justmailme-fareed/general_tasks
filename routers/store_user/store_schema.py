from mongoengine import *
from enum import Enum
from datetime import datetime

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
    parttime='parttime'
    contract='contract'

class storeDetails(EmbeddedDocument):
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    dob = StringField(required=True)
    blood_group = EnumField(Blood_group,required=True)
    gender = EnumField(Gender,required=True)
    door_number=IntField(required=True)
    street_name=StringField(required=True)
    area=StringField(required=True)
    city=StringField(required=True)
    state=StringField(required=True)
    pincode=IntField(required=True)
    aadhar_number=IntField(required=True)

class BankDetail(EmbeddedDocument):
    bank_name = StringField(required=True)
    branch_name = StringField(required=True)
    account_number=IntField(required=True)
    ifsc_code=StringField(required=True)
  
class ContactDetail(EmbeddedDocument):
    phone=StringField(required=True)
    alternate_phone=StringField()
    email=EmailField(required=True)
   
class SupportiveDocument(EmbeddedDocument):
    user_image_url = StringField()
    aadhar_image_url = StringField()
    bank_passbook_url = StringField()

class store_employee(Document):
    personal_detail = EmbeddedDocumentField(storeDetails)
    bank_detail = EmbeddedDocumentField(BankDetail)
    contact_detail=EmbeddedDocumentField(ContactDetail)
    supportive_document = EmbeddedDocumentField(SupportiveDocument)
    user_type=StringField(required=True)
    status=EnumField(store_status,default=store_status.A,required=True)
    password=StringField(requird=True)
    created_at=DateTimeField(requird=True,default=datetime.now())
    updated_at=DateTimeField(requird=True,default=datetime.now())
    created_by=ObjectIdField(requird=True)
    updated_by=ObjectIdField(requird=True)
    store_id=ObjectIdField(requird=True)
    employee_id=StringField(requird=True)

