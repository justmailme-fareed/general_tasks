"""
FileName : validation.py
Description : This is common validation file
Created Date :  27-03-2023
"""
import re

decimal_check = re.compile('^\d{0,8}(\.\d{1,50})?$')
class validation:
    def address_validation(address,start,end,error_name):  
        address = address.strip()
        if address == "":
            raise ValueError('address field required')
        if len(address) < start or  len(address) > end:
            raise ValueError(f'{error_name} field must be {start} - {end} characters')
        else:
            return " ".join(address.split())
    
    def addr_distance_validation(number):
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

    def lat_long_number_validation(number):
        number_str = str(number)
        if number_str == "":
            raise ValueError(f'Co ordinates field required')
        if decimal_check.match(number_str):
            if number <= 0:
                raise ValueError(f'Co ordinates must be greater than 0')
            return number
        else:
            raise ValueError(f'Co ordinates not a valid decimal number')