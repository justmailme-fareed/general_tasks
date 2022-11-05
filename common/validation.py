"""
FileName : validation.py
Description : This is common validation file
Author : Tree Integrated services
Created Date : 30-9-2022
"""
import re
from fastapi import  HTTPException
class validation:
    """pincode Validation"""
    def pincode_validation(v):
        # BNZAA2318J
        pincode_regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
        pincode_compile = re.compile(pincode_regex)
        if(v == None):
            raise HTTPException(status_code=422, detail="Please enter valid pincode  ")
        pin_match = re.match(pincode_compile, str(v))
        if pin_match is None:
            raise HTTPException(status_code=422, detail="Please enter valid pincode  ")
        else:
            return int(v)
    
    """aadhar Validation"""
    def aadhar_validation(v):
        aadhar_regex = ("^[2-9]{1}[0-9]{3}\\" +
             "s[0-9]{4}\\s[0-9]{4}$")
        aadhar_compile = re.compile(aadhar_regex)
        if (v == None):
            raise HTTPException(status_code=422, detail="Please enter valid aadhar number  ")
        if(re.search(aadhar_compile, v)):
            return v
        else:
            raise HTTPException(status_code=422, detail="Please enter valid aadhar number  ")

    #Driving license validation
    def drivinglicense_validation(v):
        driving_license_regex = ("^(([A-Z]{2}[0-9]{2})" +
             "( )|([A-Z]{2}-[0-9]" +
             "{2}))((19|20)[0-9]" +
             "[0-9])[0-9]{7}$")
        driving_license_compile= re.compile(driving_license_regex)
        if (v == None):
            raise HTTPException(status_code=422, detail="Please enter valid aadhar number  ")
        if(re.search(driving_license_compile, v)):
            return v
        else:
            raise HTTPException(status_code=422, detail="Please enter valid aadhar number  ")
      
    """Mobile Number Validation"""
    def mobile_validate(mobile_number,bool_value,module_name):
        if mobile_number:
            if bool_value == False:
                mobile_number="null"
                return mobile_number
            else:
                mobile_number = mobile_number.strip()
                mobile_pattern = re.compile("(0|91)?[6-9][0-9]{9}")
                if mobile_pattern.match(mobile_number):
                    return mobile_number
                else:
                    raise HTTPException(status_code=422, detail=f"Please enter valid {module_name}")
    
    #IFSC code validation
    def ifsc_code_validation(ifsc_code):
        # SBIN0125620
        ifsc_regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
        ifsc_compile= re.compile(ifsc_regex)
        if(ifsc_code == None):
            raise HTTPException(status_code=422, detail="Please enter valid ifsc_code")
        if(re.search(ifsc_compile, ifsc_code)):
            return ifsc_code
        else:
            raise HTTPException(status_code=422, detail="Please enter valid ifsc_code")
    
    #validation for firstname,lastname,city,are,bankname,branchname,state,strreetname,
    def name_validation(v,module_name,start_limit,end_limit):
        special_character_check =  re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        v = v.strip()
        if v == "":
            raise HTTPException(status_code=422, detail=f'{module_name} field required')
        if special_character_check.search(v) != None:
            raise HTTPException(status_code=422, detail=f'Special characters not allowed on {module_name} field')
        if len(v) < start_limit or  len(v) > end_limit:
            raise HTTPException(status_code=422, detail=f'{module_name} field {start_limit} - {end_limit} letters only allowed')
        return "".join(v.split())


