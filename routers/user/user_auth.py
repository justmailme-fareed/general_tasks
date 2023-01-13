"""
FileName : user_auth.py
Description : User JWT authentication present here.
Author : Tree Integrated services
Created Date : 30-9-2022
"""

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from configuration.config import secret,algorithm,minute,day
from .user_schema import StoreUser
import json

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = secret

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=day, minutes=minute),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=algorithm
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[algorithm])
            get_user_data = StoreUser.objects(store_id= payload['sub'])
            get_user_data = get_user_data.to_json()
            data = json.loads(get_user_data)
            # print(data)
            # return data
            return {"name":payload['sub'],"id":data[0]["_id"]["$oid"]}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)