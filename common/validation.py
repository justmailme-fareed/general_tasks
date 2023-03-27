"""
FileName : validation.py
Description : This is common validation file
Created Date :  27-03-2023
"""
import re

class validation:
    def address_validation(address,start,end,error_name):  
        address = address.strip()
        if address == "":
            raise ValueError('picode field required')
        if len(address) < start or  len(address) > end:
            raise ValueError(f'{error_name} field must be {start} - {end} characters')
        else:
            return " ".join(address.split())
    
    def distance_validation(number):
        number_str = str(number)
        number_str = number_str.strip()
        if number_str == "":
            raise ValueError('distance field required')
        if number_str.isnumeric:
            if len(number_str) <=10:
                   return number
            else:
                raise ValueError('distance is must be below 10km')
        else:
            raise ValueError('distance not a valid number')
