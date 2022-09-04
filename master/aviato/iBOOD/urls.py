
from django.urls import path


from . import views


urlpatterns = {
    path("",views.home,name="iBOOD_home"),
    path("<int:id>",views.search,name="ibood_searches"),
}

