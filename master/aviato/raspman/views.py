from json import load
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import os

# Create your views here.

def index(request):
    template = loader.get_template('raspman/raspman.html')
    return HttpResponse(template.render({},request))


def shutting_down(request):
    os.system("sudo shutdown -h now")
    return HttpResponse("Shutting down")

def restarting(request):
    os.system("sudo reboot")
    return HttpResponse("Restarting the Raspberry Pi")

