from django.contrib import admin
from django.urls import URLPattern, include, path
from django.conf.urls import *
from planningUY import views

urlpatterns = [
    path('planningUY/', include('planningUY.urls')),
    path('planningUY/', views.home),
]
