# User/urls.py

from django.urls import path
from . import views  # Import your views


urlpatterns = [
    path('users/', views.list_users, name='list_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/add/', views.add_user, name='sign-up'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    
    
    path('clients/', views.list_clients, name='list_clients'),
    path('professionals/', views.list_professionals, name='list_professionals'),
    path('providers/', views.list_providers, name='list_providers'),
    path('admins/', views.list_admins, name='list_admins'),
    
    path('clients/add/', views.add_client, name='add_client'),
    path('professionals/add/', views.add_professional, name='add_professional'),
    path('providers/add/', views.add_provider, name='add_provider'),
    path('admins/add/', views.add_admin, name='add_admin'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
]
