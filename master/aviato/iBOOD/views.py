from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.


def home(request):
    return HttpResponse("home page iBood")