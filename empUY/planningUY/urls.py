from django.contrib import admin
from django.urls import URLPattern, include, path
from django.conf.urls import *
from planningUY import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginU, name='login'),
    path('logout/', views.logoutU, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]