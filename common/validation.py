"""
FileName : validation.py
Description : This is common validation file
Author : Tree Integrated services
Created Date : 30-9-2022
"""
import re
from fastapi import HTTPException

special_character_check =  re.compile('[@_!;,`#$%^&*()<>?/\|}{~:]')
objectID_check =  re.compile('^[0-9a-fA-F]{24}$')
decimal_check = re.compile('^\d{0,8}(\.\d{1,4})?$')

class validation:
    """pincode Validation"""
    def pincode_validation(v):
        # BNZAA2318J
        pincode_regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
        pincode_compile = re.compile(pincode_regex)
        if(v == None):
            raise HTTPException(status_code=422, detail="Please enter valid pincode")
        pin_match = re.match(pincode_compile, str(v))
        if pin_match is None:
            raise HTTPException(status_code=422, detail="Please enter valid pincode")
        else:
            return int(v)
    
    """aadhar Validation"""
    def aadhar_validation(v):
        aadhar_regex = ("^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}$")
        aadhar_compile = re.compile(aadhar_regex)
        if (v == None):
            raise HTTPException(status_code=422, detail="Please enter valid aadhar number")
        if(re.search(aadhar_compile, v)):
            return v
        else:
            raise HTTPException(status_code=422, detail="Please enter valid aadhar number")

    #Driving license validation
    def drivinglicense_validation(v):
        driving_license_regex = ("^(([A-Z]{2}[0-9]{2})" +"( )|([A-Z]{2}-[0-9]" +"{2}))((19|20)[0-9]" +"[0-9])[0-9]{7}$")
        driving_license_compile= re.compile(driving_license_regex)
        if (v == None):
            raise HTTPException(status_code=422, detail="Please enter valid driving license number")
        if(re.search(driving_license_compile, v)):
            return v
        else:
            raise HTTPException(status_code=422, detail="Please enter valid driving license number")
      
    """Mobile Number Validation"""
    def mobile_validate(mobile_number,bool_value,module_name):
        if mobile_number:
            if bool_value == False:
                mobile_number="null"
                return mobile_number
            else:
                mobile_number = mobile_number.strip()
                mobile_pattern = re.compile("^[789]\d{9}$")
                if mobile_pattern.match(mobile_number):
                    return "".join(mobile_number.split())
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
        #special_character_check =  re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        v = v.strip()
        if v == "":
            raise HTTPException(status_code=422, detail=f'{module_name} field required')
        if special_character_check.search(v) != None:
            raise HTTPException(status_code=422, detail=f'Special characters not allowed in {module_name} field')
        if len(v) < start_limit or  len(v) > end_limit:
            raise HTTPException(status_code=422, detail=f'{module_name} field {start_limit} - {end_limit} letters only allowed')
        return "".join(v.split())
    # account number validation
    def account_number_validation(v):
        if len(str(v)) != 11:
            raise HTTPException(status_code=422, detail=f'Please enter valid account number')
        return int(v)

    """ Decimal Number Validation"""
    def decimal_number_validate(number,error_name):
        number_str = str(number)
        if number_str == "":
            raise ValueError(f'{error_name} field required')
        if decimal_check.match(number_str):
            return number
        else:
            raise ValueError(f'{error_name} not a valid decimal number')

    """ObjectID Validation"""
    def objectID_validate(obj_id,error_name):  
        obj_id = obj_id.strip()
        if obj_id == "":
            raise ValueError(f'{error_name} field required')
        if objectID_check.match(obj_id):
            return " ".join(obj_id.split())
        else:
            raise ValueError(f'Invalid objectid for {error_name} field')
        
        """Name Validation"""
    def text_name_validate(name,start,end,error_name):  
        name = name.strip()
        if name == "":
            raise ValueError(f'{error_name} field required')
        if len(name) < start or  len(name) > end:
            raise ValueError(f'{error_name} field {start} - {end} letters only allowed')
        if special_character_check.search(name) != None:
            raise ValueError(f'Special characters not allowed on {error_name} field')
        return " ".join(name.split())

"""Common Validation"""
class form_validation:
    """Name Validation"""
    def form_name_validate(name,start,end,error_name):  
        name = name.strip()
        if len(name) < start or  len(name) > end:
            raise ValueError(f'{error_name} field must be {start} - {end} letters')
        if special_character_check.search(name) == None:
            return " ".join(name.split())
        else:
            raise ValueError(f'Special characters are not allowed on {error_name} field')


