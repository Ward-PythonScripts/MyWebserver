from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import json

from . import ibood_db
from .ibood_scraper import POSSIBLE_FILTERS

def home(request):
    

    if request.method == 'POST':
        data = request.POST
        if not check_if_edit_recipient_post(data):
            if not check_if_remove_recipient_post(data):
                if not check_if_add_recipient_post(data):
                    if not check_if_search_change_post(data):
                        print("Tried to post something but couldn't figure out what it was")

    #get the recipients from the database
    recipients = ibood_db.get_all_recipients()
    context = {
        'recipients': recipients,
        'possible_filters':POSSIBLE_FILTERS,
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


    


def search(request,id):
    if request.method == 'POST':
        data = request.body.decode("UTF-8")
        print("data is ",data)
        if not check_if_search_change_post(data):
            print("Tried to post something but couldn't figure out what it was")


    recipient = ibood_db.get_recipient_with_id(id)
    context = {
        'recipient':recipient,
        'possible_filters':POSSIBLE_FILTERS,
    }
    template = loader.get_template('ibood/ibood_searches.html')
    return HttpResponse(template.render(context,request))



def check_if_search_change_post(data):

    # data = list(data.keys())[0]
    # print("in func data is ",data)
    json_data = json.loads(data)
    if json_data.get('type') == 'search':
        id = json_data.get('id')
        if id == 'new_id':
            #want to add a new search to the db
            #first check if we have all the correct values
            name = json_data.get('name')
            filters = json_data.get('filters')
            recipient_id = json_data.get('recipientId')
            ibood_db.add_search(recipient_Id=recipient_id,search_action=json.dumps(filters),name=name)
        else:
            filters = json_data.get('filters')
            name = json_data.get('name')
            ibood_db.update_search(json.dumps(filters),id,name)
        return True
    else:
        return False
