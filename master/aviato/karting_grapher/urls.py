from django.urls import path

from . import views

urlpatterns = {
    path("",views.karting_home,name="karting_home"),
    path("new_time/",views.karting_add_new_time,name="karting_new_time"),

}