# User/urls.py

from django.urls import path
from . import views  # Import your views
from .views import  *
from django.contrib.auth.views import LoginView, LogoutView , PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('users/', views.list_users, name='list_users'),
    path('users/<int:user_id>/', views.user_detail_update, name='user_detail_update'),
    path('users/add/', views.add_user, name='sign-up'),
    
    path('clients/', views.list_clients, name='list_clients'),
    path('professionals/', views.list_professionals, name='list_professionals'),
    path('providers/', views.list_providers, name='list_providers'),

    
    path('clients/add/', views.add_client, name='sign-up'),
    path('professionals/add/', views.add_professional, name='sign-up-prof'),
    path('providers/add/', views.add_provider, name='sign-up-prov'),

    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    path('login/', Login.as_view() , name="login" ),

    path('logout/', LogoutView.as_view(), name='logout'),  # Adds the logout route

    #path('verify-email/<str:token>/', verify_email, name='verify_email'),

    path('verify-code/', views.verify_verification_code, name='verify_verification_code'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Ensure correct name
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
