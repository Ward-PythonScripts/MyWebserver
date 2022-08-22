from http.client import HTTPResponse
import re
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


# Create your views here.

def index(request):
    template = loader.get_template('home/index.html')
    context = {
        'smt': None
    }
    return HttpResponse(template.render({},request))