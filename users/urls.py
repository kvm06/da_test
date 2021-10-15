from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('clients/create', views.create, name='create')
]