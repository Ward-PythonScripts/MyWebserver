#https://realpython.com/django-social-post-3/ <-- hopefully how to post in django

from calendar import c
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from . import notifier_backend
# Create your views here.

def index(request):

    if request.method == 'POST':
        data = request.POST
        name = data.get('name_edit')
        mail = data.get('mail_edit')
        id = data.get('id')
        if name and mail and id is not None:
            #an edit button was clicked
            notifier_backend.update_recipient(name,mail,id)
        else:
            id = data.get('remove')
            if id is not None:
                #a button to remove a recipient was clicked
                print("They are trying to remove the recipient",id)
                notifier_backend.remove_recipient(id)
            else:
                mail = data.get('mail') 
                name = data.get('name')
                if mail and name is not None:
                    #want to add a new recipient to the list
                    notifier_backend.add_recipient(name=name,mail=mail)

                    
            

    #get the recipients from the database
    recipients = notifier_backend.get_all_recipients()
    categories = notifier_backend.get_categories()
    context = {
        'recipients': recipients,
        'categories':categories
    }
    template = loader.get_template('notifier/notifier_home.html')
    return HttpResponse(template.render(context,request))
