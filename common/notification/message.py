###################################### Mail Service Section #######################

data={}
message=''
title=''
def get_general_txt_mail_message(msg_type):
    if msg_type=="welcome":
        title='Trees.in'
        message="Hi,"+'\n\n\n'+"Thank you for signing up for Trees. We appreciate your interest."+'\n\n'+"We will do our best to provide our services."
    return {'title':title,'mail_text':message,'body':None}

def get_general_html_mail_message(msg_type):
    if msg_type=="welcome":
        title='Trees.in'
        message="Hi,"+'\n\n\n'+"Thank you for signing up for Trees. We appreciate your interest."+'\n\n'+"We will do our best to provide our services."
    return {'title':title,'body':message,'mail_text':None}