from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('clients/create', views.create, name='create'),
    path('clients/login', views.log_in, name='login'),
    path('clients/logout', views.log_out, name='logout')
]