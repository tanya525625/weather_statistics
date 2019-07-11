from django.conf.urls import url
from . import views
from django.urls import include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^forms.py', views.index, name='statics'),
]
