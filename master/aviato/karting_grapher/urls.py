from django.urls import path

from . import views

urlpatterns = {
    path("",views.karting_home,name="karting_home"),
    path("new_time/",views.karting_add_new_time,name="karting_new_time"),
    path("sessions/",views.show_default_session),
    path("sessions/<int:session_index>",views.show_specific_sessions,name="karting_session"),
    path("driver/",views.show_driver),
    path("head_to_head/",views.head_to_head),
    path("kart/",views.show_kart),


}