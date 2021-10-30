from django.urls import path   
from . import views

urlpatterns = [
    path('login/' , views.login, name = 'login'),
    path('logout/' , views.logout, name = 'logout'),
    path('get_password/' , views.get_password, name = 'get_password'),
]