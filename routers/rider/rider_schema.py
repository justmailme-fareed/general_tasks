from mongoengine import *
from enum import Enum
class Gender(str,Enum):
    male="male"
    female="female"
    others="others"
   
class User_type(str,Enum):
    rider='rider'
    store='store'
    user='user'

class store_status(str,Enum):
    A='A'
    I='I'
    B='B'
    D='D'
    L='L'



class Blood_group(str,Enum):
    A='A+'
    a='A-'
    B='B+'
    b='B-'
    AB='AB+'
    ab='AB-'
    O='O+'
    o='O-'

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
    language_known=StringField(required=True)
    door_number=IntField(required=True)
    street_name=StringField(required=True)
    area=StringField(required=True)
    city=StringField(required=True)
    state=StringField(required=True)
    pincode=IntField(required=True)
    aadhar_number=IntField(required=True)

class BankDetail(Document):
    bank_name = StringField(required=True,min_length=3,max_length=20)
    branch_name = StringField(required=True,min_length=3,max_length=20)
    account_number=IntField(required=True,min_length=11,max_length=11)
    ifsc_code=StringField(required=True)
  
class ContactDetail(Document):
    phone=IntField(required=True,min_length=10,max_length=10)
    alternate_phone=IntField(required=True,min_length=10,max_length=10)
    job_type = EnumField(Jobtype,required=True)
    email=EmailField(required=True)

class DrivingDetail(Document):
        driving_license_number=IntField(required=True)
        phodriving_license_expiry_datene=StringField(required=True)


class  EmployeeDetail(Document):
    user_type=EnumField(User_type,requird=True)
    store_status=EnumField(store_status,requird=True)
    password=StringField(requird=True)
    created_at=StringField(requird=True)
    updated_at=StringField(requird=True)
    created_by=StringField(requird=True)
    updated_by=StringField(requird=True)
    store_id=StringField(requird=True)
    employee_id=StringField(requird=True)

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
    employee_detail = ReferenceField(EmployeeDetail)

class images(Document):
    aadhar_image_url=StringField()