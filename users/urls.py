from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('clients/create', views.create, name='create'),
    path('clients/login', views.log_in, name='login'),
    path('clients/logout', views.log_out, name='logout'),
    path('clients/<int:user_id>', views.user_profile, name='user_profile'),
    path('clients/<int:user_id>/match', views.match, name='match'),
    path('clients/list', views.users_list, name='users_list'),
]
