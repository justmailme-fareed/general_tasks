"""
FileName : address.py
Description : This file manage address section.
Created Date : 27-03-2023
"""

from fastapi import APIRouter,Depends,Response,status,Request,Form
from .address_schema  import user_address,user_address_schema
from configuration.config import api_version
from database.connection import *
import logging
from common.validation import validation
from geopy.distance import great_circle as GRC
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session
from sqlalchemy import asc

router = APIRouter(
    prefix=api_version + "/user",
    tags=["Address"],
    responses={404: {"description": "Not found"}},
)


#Create user address details
@router.post('/address', status_code=201)
def create_user_address(response : Response,request: Request,address_details:user_address_schema,db: Session = Depends(get_db)):
    try:
        addr_details_exist=db.query(user_address).where(user_address.address==address_details.address).count()
        if addr_details_exist > 0:
            response.status_code = 409
            return {"status":"error","message":f"address name already exists"}
        user_addr = user_address()
        user_addr.address = address_details.address
        user_addr.latitude = address_details.latitude
        user_addr.longitude = address_details.longitude
        db.add(user_addr)
        db.commit()
        return {'status': "success", "message" :f"address added successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}
    
#get user address details
@router.get('/address', status_code=200)
def get_user_address(response : Response,skip:int=0,limit:int=100,db: Session = Depends(get_db)):
    try:
        data=db.query(user_address).order_by(asc(user_address.id)).offset(skip).limit(limit).all()
        return {'status': "success","data": data}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#get user address details by id
@router.get('/address/{id}', status_code=200)
def get_user_address_by_id(response : Response,id:int,db: Session = Depends(get_db)):
    try:
        data=db.query(user_address).where(user_address.id==id).first()
        if data is None:
            response.status_code = 404
            return {"status":"error","message":f"No address found for given address id {id}"}
        return {'status': "success","data": data}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#update user address details
@router.put('/address/{id}', status_code=200)
def update_user_address(response : Response,address_details:user_address_schema,id:int,db: Session = Depends(get_db)):
    try:
        user_addr_details=db.query(user_address).where(user_address.id==id).first()
        if user_addr_details is None:
            response.status_code = 404
            return {"status":"error","message":f"No address found for given address id {id}"}
        addr_details_exist=db.query(user_address).where((user_address.id != id) & (user_address.address==address_details.address)).count()
        if addr_details_exist > 0:
            response.status_code = 409
            return {"status":"error","message":f"address name already exists"}
        user_addr_details.address = address_details.address
        user_addr_details.latitude = address_details.latitude
        user_addr_details.longitude = address_details.longitude
        db.add(user_addr_details)
        db.commit()
        return {'status': "success", "message" :f"address updated successfully"}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#delete user address details
@router.delete('/address/{id}', status_code=200)
def delete_user_address(response : Response,id:int,db: Session = Depends(get_db)):
    try:
        data=db.query(user_address).where(user_address.id==id).first()
        if data is None:
            response.status_code = 404
            return {"status":"error","message":f"No address found for given address id {id}"}
        db.query(user_address).where(user_address.id == id).delete()
        db.commit()
        return {'status': "success","message": 'address deleted succssfully'}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

#get user all address for given location
@router.get('/address_by_distance', status_code=200)
def get_user_address_by_distance(response : Response,latitude:float,longitude:float,distance:int,db: Session = Depends(get_db)):
    try:
        address_list = []
        distance=validation.addr_distance_validation(distance)
        latitude=validation.lat_long_number_validation(latitude)
        longitude=validation.lat_long_number_validation(longitude)
        
        user_location=(latitude,longitude)
        data=db.query(user_address).all()
        if data is None:
            response.status_code = 404
            return {"status":"error","message":"No address added,please add new address"}
        for addr in data:
            addr_latitude = addr.latitude
            addr_longitude = addr.longitude
            addr_lat_lon = (addr_latitude,addr_longitude)
            try:
                user_distance = GRC(user_location,addr_lat_lon).km
            except:
                response.status_code = 422
                return {"status":"error","message":"Invalid location coordinates"}
            user_distance = round(user_distance, 1)
            if user_distance <= distance:
                data = {
                        "address":addr.address,
                        "latitude":addr.latitude,
                        "longitude":addr.longitude,
                }
                address_list.append(data)
        return {'status': "success","data": address_list}
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return { 'status': "error","message" :str(e)}

