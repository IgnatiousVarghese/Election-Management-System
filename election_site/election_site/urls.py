
from django.contrib import admin
from django.urls import path, include   
from . import views
from election import views_authenticate 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('login/' , views_authenticate.login, name = 'login'),
    path('logout/' , views_authenticate.logout, name = 'logout'),
    path('get_password/' , views_authenticate.get_password, name = 'get_password'),
    
    path('home/', include('election.urls')),
    
    path('result/', views.result, name = 'result'),
]
