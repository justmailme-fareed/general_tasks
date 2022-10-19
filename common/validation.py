"""
FileName : validation.py
Description : This is common validation file
Author : Tree Integrated services
Created Date : 30-9-2022
"""

import re 

"""Common Validation"""
class validation:
    """Name Validation"""
    def name_validate(name,start,end,error_name):  
        name = name.strip()
        special_character_check =  re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if name == "":
            raise ValueError(f'{error_name} field required')
        if len(name) < start or  len(name) > end:
            raise ValueError(f'{error_name} field {start} - {end} letters only allowed')
        if special_character_check.search(name) != None:
            raise ValueError(f'Special characters not allowed on {error_name} field')
        return " ".join(name.split())

    """Mobile Number Validation"""
    def mobile_validate(number,error_name):
        number = number.strip()
        if number == "":
            raise ValueError(f'{error_name} field required')
        mobile_pattern = re.compile("(0|91)?[6-9][0-9]{9}")
        if mobile_pattern.match(number):
            return number
        else:
            raise ValueError(f'{error_name} not a valid format')

    """Email Validation"""
    def email_validate():
        pass
