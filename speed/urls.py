from django.contrib import admin
# from django.conf.urls import re_path
from django.urls import path, re_path
from speed import views

urlpatterns = [
    re_path(r'^auth/login/', views.login, name='login-api'),
    re_path(r'^auth/logout/', views.logout, name='logout-api'),
    re_path(r'^profile/(?P<username>.+)/', views.profile, name='profile-api'),
    re_path(r'^profile/', views.profile, name='profile-api'),
    re_path(r'^speed_limit/$', views.get_speed_limit, name='speed_limit-detail-get-api'),
    # re_path(r'^speed_limit/(?P<lat>[-+]?[0-9]*\.?[0-9]+)/(?P<long>[-+]?[0-9]*\.?[0-9]+)/$', views.get_speed_limit, name='speed_limit-detail-get-api'),
    re_path(r'^penalty/', views.penalty, name='penalty'),
    re_path(r'^vehicles/', views.vehicles, name='vehicles'),
    # re_path(r'^penalty/', views.StudentList.as_view(), name='penalty'),

]
