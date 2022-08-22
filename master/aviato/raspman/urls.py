from django.urls import path

from . import views

urlpatterns = {
    path("",views.index,name="raspman_home"),
    path("shutting_down/",views.shutting_down,name="raspman_shutdown"),
    path("restarting/",views.restarting,name="raspman_restart"),
}