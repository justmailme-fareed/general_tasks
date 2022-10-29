"""
FileName : validation.py
Description : This is common validation file
Author : Tree Integrated services
Created Date : 30-9-2022
"""

from email import message
import re
from fastapi import FastAPI, HTTPException

speical_char=['!','@','#','$','%','^','&','*','+','=','(',')','{','}','[',']',':',' ']

        
import re 

"""Common Validation"""
class validation:
    """Name Validation"""
    def name_validation(v):
        v= "".join(v.split())
        if v == '':
            raise HTTPException(status_code=404, detail="Please enter name")
        elif len(v)>20:
            raise HTTPException(status_code=404, detail="Please enter valid name  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid name  ")

        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid name")

        return v
    
    def lastname_validation(v):
        v= "".join(v.split())
        if v == '':
            raise HTTPException(status_code=404, detail="Please enter lastname")
        elif len(v)>20:
            raise HTTPException(status_code=404, detail="Please enter valid lastname  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid lastname  ")

        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid lastname")
        return v
    def street_name_validation(v):
        v= "".join(v.split())
        if v == '':
            raise HTTPException(status_code=404, detail="Please enter street_name")
        elif len(v)>20:
            raise HTTPException(status_code=404, detail="Please enter valid street_name  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid street_name  ")

        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid street_name")
        return v


    def area_validation(v):
        v= "".join(v.split())
        if v == '':
            raise HTTPException(status_code=404, detail="Please enter area")
        elif len(v)>20:
            raise HTTPException(status_code=404, detail="Please enter valid area  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid area  ")

        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid area")
        return v


    
    def city_validation(v):
        v= "".join(v.split())
        if v == '':
            raise HTTPException(status_code=404, detail="Please enter city")
        elif len(v)>20:
            raise HTTPException(status_code=404, detail="Please enter valid city  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid city  ")

        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid city")
        return v
    
    

    def state_validation(v):
        v= "".join(v.split())
        if v == '':
            raise HTTPException(status_code=404, detail="Please enter state")
        elif len(v)>20:
            raise HTTPException(status_code=404, detail="Please enter valid state  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid state  ")

        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid state")
        return v
    def pincode_validation(v):
        # BNZAA2318J
        regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
        p = re.compile(regex)
        if(v == None):
            raise HTTPException(status_code=404, detail="Please enter valid pincode  ")
        m = re.match(p, str(v))
        if m is None:
            raise HTTPException(status_code=404, detail="Please enter valid pincode  ")
        else:
            return int(v)
    
    def aadhar_validation(v):
        regex = ("^[2-9]{1}[0-9]{3}\\" +
             "s[0-9]{4}\\s[0-9]{4}$")
        p = re.compile(regex)
        if (v == None):
            raise HTTPException(status_code=404, detail="Please enter valid aadhar number  ")
        if(re.search(p, v)):
            return v
        else:
            raise HTTPException(status_code=404, detail="Please enter valid aadhar number  ")


    def drivinglicense_validation(v):
        regex = ("^(([A-Z]{2}[0-9]{2})" +
             "( )|([A-Z]{2}-[0-9]" +
             "{2}))((19|20)[0-9]" +
             "[0-9])[0-9]{7}$")
     
        p = re.compile(regex)
        if (v == None):
            raise HTTPException(status_code=404, detail="Please enter valid aadhar number  ")
 
        if(re.search(p, v)):
            return v
        else:
            raise HTTPException(status_code=404, detail="Please enter valid aadhar number  ")

    def door_number(v):
        if v == '':
            raise HTTPException(status_code=404, detail="Please enter door_number")
       
    """Mobile Number Validation"""
    def mobile_validate(number):
        number = number.strip()
        if number == "":
            raise HTTPException(status_code=404, detail="Please enter valid phone number  ")
        mobile_pattern = re.compile("(0|91)?[6-9][0-9]{9}")
        if mobile_pattern.match(number):
            return number
        else:
            raise HTTPException(status_code=404, detail="Please enter valid phone number  ")


    def alternatephone_validate(number):
        if number is None:
            number="null"
            return number
        else:

            number = number.strip()
            if number:
                mobile_pattern = re.compile("(0|91)?[6-9][0-9]{9}")
                if mobile_pattern.match(number):
                    return number
                else:
                    raise HTTPException(status_code=404, detail="Please enter valid alternate number  ")

        # if number == "":
        #     return number
        #     # raise HTTPException(status_code=404, detail="Please enter valid alternate number  ")
        # # if number:
        #     mobile_pattern = re.compile("(0|91)?[6-9][0-9]{9}")
        #     if mobile_pattern.match(number):
        #         return number
        #     else:
        #         raise HTTPException(status_code=404, detail="Please enter valid alternate number  ")



    def account_number_validation(v):
        if len(str(v))<11:
            raise HTTPException(status_code=404, detail="Please enter valid account_number  ")

        return int(v)


    def ifsc_code_validation(v):
        # SBIN0125620
        regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
        p = re.compile(regex)
        if(v == None):
            raise HTTPException(status_code=404, detail="Please enter valid ifsc_code  ")
        if(re.search(p, v)):
            return v
        else:
            raise HTTPException(status_code=404, detail="Please enter valid ifsc_code  ")

    def bank_name_validation(v):
        v= "".join(v.split())

        if v == '':
            raise HTTPException(status_code=404, detail="Please enter bankname")
        elif len(v)>20:
            raise HTTPException(status_code=404, detail="Please enter valid bankname  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid bankname  ")
        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid name")

        return v

     
    def branch_name_validation(v):
        v= "".join(v.split())

        if v == '':
            raise HTTPException(status_code=404, detail="Please enter branch_name")
        elif len(v)>20 or len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid branch_name  ")

        elif len(v)<3:
            raise HTTPException(status_code=404, detail="Please enter valid branch_name  ")
        for i in v:
            if i in speical_char:
                raise HTTPException(status_code=404, detail="Please enter valid name")
        return v


    """Email Validation"""
    def email_validate():
        pass
