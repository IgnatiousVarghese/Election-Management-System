# This file is for linking the urls with their corresponding functions in views file.

from django.urls import path
from . import views

app_name = 'election'
urlpatterns = [
    path('' , views.home, name = 'home'),

    path('view-post/<int:idpost>/' , views.view_post, name = 'view_post'),
    path('vote/<int:idpost>/<slug:idcandidate>' , views.vote, name = 'vote'),

    path('edit-manifesto/', views.edit_manifesto, name = 'edit_manifesto'),

    path('start-election/', views.start_election, name = 'start_election'),
    path('end-election/', views.end_election, name = 'end_election'),

    path('add-candidate/', views.add_candidate, name = 'add_candidate'),
    path('add-post/', views.add_post, name = 'add_post'),

    path('search-candidate/', views.search_candidate, name = 'search_candidate'),
    path('del-candidate/', views.del_candidate, name = 'del_candidate'),
    path('search-post/', views.search_post, name = 'search_post'),
    path('del-post/', views.del_post, name = 'del_post'),
]