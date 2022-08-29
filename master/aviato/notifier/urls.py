

from django.urls import path


from . import views


urlpatterns = {
    path("",views.index,name="notifier_home"),
}

