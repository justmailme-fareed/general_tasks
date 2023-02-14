from mongoengine import *
from enum import Enum
from datetime import datetime
from bson.objectid import ObjectId




class todos(Document):
    todo_name=StringField(requird=True)
    created_at=DateTimeField(required=True,default=datetime.now())
    updated_at=DateTimeField(required=True,default=datetime.now())

    