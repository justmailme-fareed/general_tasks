"""
FileName : address.py
Description : This file manage address section.
Created Date : 27-03-2023
"""

from fastapi import APIRouter,Depends,Response,status,Request,Form
from .address_schema  import user_address
from configuration.config import api_version
from database.connection import *
import logging
import json
import datetime
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
def create_user_address(response : Response,request: Request,address:str = Form(),db: Session = Depends(get_db)):
    try:
        address=validation.address_validation(address,3,50,'address')
        geolocator = Nominatim(user_agent="eastvantage")
        location = geolocator.geocode(address)
        if location is None:
            response.status_code = 404
            return {"status":"error","message":"Location not found,Please search for a different location"}
        user_addr = user_address()
        user_addr.address = address
        user_addr.latitude = location.latitude
        user_addr.longitude = location.longitude
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

#update user address details
@router.put('/address/{id}', status_code=200)
def update_user_address(response : Response,id:int,address:str = Form(),db: Session = Depends(get_db)):
    try:
        user_addr_details=db.query(user_address).where(user_address.id==id).first()
        if user_addr_details is None:
            response.status_code = 404
            return {"status":"error","message":f"No address found for given address id {id}"}
        address=validation.address_validation(address,3,50,'address')
        geolocator = Nominatim(user_agent="eastvantage")
        location = geolocator.geocode(address)
        if location is None:
            response.status_code = 404
            return {"status":"error","message":"Location not found,Please search for a different location"}
        user_addr_details.address = address
        user_addr_details.latitude = location.latitude
        user_addr_details.longitude = location.longitude
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
        raise SystemExit('d')
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
def get_user_address_by_distance(response : Response,address:str,distance:int,db: Session = Depends(get_db)):
    try:
        address_list = []
        address=validation.address_validation(address,3,50,'address')
        distance=validation.distance_validation(distance)
        geolocator = Nominatim(user_agent="eastvantage")
        location = geolocator.geocode(address)
        if location is None:
            response.status_code = 404
            return {"status":"error","message":"Location not found,Please search for a different location"}
        user_location=(float(location.latitude),float(location.longitude))
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

