# User/urls.py

from django.urls import path
from . import views  # Import your views
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path('users/', views.list_users, name='list_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/add/', views.add_user, name='sign-up'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    
    
    path('clients/', views.list_clients, name='list_clients'),
    path('professionals/', views.list_professionals, name='list_professionals'),
    path('providers/', views.list_providers, name='list_providers'),

    
    path('clients/add/', views.add_client, name='sign-up'),
    path('professionals/add/', views.add_professional, name='sign-up-prof'),
    path('providers/add/', views.add_provider, name='sign-up-prov'),

    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    path('login/', LoginView.as_view(template_name='User/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
]
