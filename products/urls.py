from django.urls import path
from . import views

urlpatterns = [
    path('products', views.parse_products, name='parse_products'),
]