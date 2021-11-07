from django.urls import path
from . import views, views_authenticate

app_name = 'election'
urlpatterns = [
    path('' , views.home, name = 'home'),

    path('view-post/<int:idpost>/' , views.view_post, name = 'view_post'),
    path('vote/<int:idpost>/<slug:idcandidate>' , views.vote, name = 'vote'),
]