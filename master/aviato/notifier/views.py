#https://realpython.com/django-social-post-3/ <-- hopefully how to post in django

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from . import notifier_backend
# Create your views here.

def index(request):

    if request.method == 'POST':
        data = request.POST
        id = data.get('edit')
        if id is not None:
            #an edit button was clicked
            print("They are trying to edit the recipient",id)
        else:
            id = data.get('remove')
            if id is not None:
                #a button to remove a recipient was clicked
                print("They are trying to remove the recipient",id)
                notifier_backend.remove_recipient(id)
            else:
                id = data.get('add')
                if id is not None:
                    #want to add a new recipient to the list
                    
            

    #get the recipients from the database
    recipients = notifier_backend.get_all_recipients()
    context = {
        'recipients': recipients
    }
    template = loader.get_template('notifier/notifier_home.html')
    return HttpResponse(template.render(context,request))
