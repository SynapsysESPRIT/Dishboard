# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_view, name='inventory-view'),  # Default path for inventory
    path('detect-ingredients/', views.detect_ingredients, name='detect-ingredients'),
    path('detect/', views.detect_ingredients, name='detect-ingredients'),


   
]

