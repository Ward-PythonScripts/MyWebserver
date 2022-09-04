from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from . import ibood_db

def home(request):

    if request.method == 'POST':
        data = request.POST
        print("data is ",data)
        if not check_if_edit_recipient_post(data):
            if not check_if_remove_recipient_post(data):
                if not check_if_add_recipient_post(data):
                    if not check_if_preference_change_post(data):
                        print("Tried to post something but couldn't figure out what it was")

    #get the recipients from the database
    recipients = ibood_db.get_all_recipients()
    context = {
        'recipients': recipients,
    }
    template = loader.get_template('ibood/ibood_home.html')
    return HttpResponse(template.render(context,request))

def check_if_edit_recipient_post(data):
    name = data.get('name_edit')
    mail = data.get('mail_edit')
    id = data.get('id')
    if name and mail and id is not None:
        #an edit button was clicked
        ibood_db.update_recipient(name,mail,id)
        return True
    else:
        return False

def check_if_remove_recipient_post(data):
    id = data.get('remove')
    if id is not None:
        #a button to remove a recipient was clicked
        ibood_db.remove_recipient(id)
        return True
    else:
        return False
def check_if_add_recipient_post(data):
    mail = data.get('mail') 
    name = data.get('name')
    if mail and name is not None:
        #want to add a new recipient to the list
        ibood_db.add_recipient(name=name,mail=mail)
        return True
    else:
        return False
def check_if_preference_change_post(data):
    return False
#     all_cb = data.get('all')
#     none_cb = data.get('none')
#     id = data.get('id')
#     if (all_cb or none_cb) and id is not None:
#         #valid
#         wants_all_mails = (all_cb is not None) #if all_cb is defined, that means that the checkbox was ticked
#         exceptions = []
#         for key in data.keys():
#             if key not in ['all','none','csrfmiddlewaretoken','id']:
#                 exceptions.append(key)
#         if wants_all_mails:
#             allowed_value = 'all'
#         else:
#             allowed_value = 'none'
#         new_pref = {
#             'allowed':allowed_value,
#             'exceptions':exceptions
#         }
#         json_string = json.dumps(new_pref)
#         notifier_backend.update_preferences(json_string,id)
#         return True
# 
    # else:
    #     return False
    
