from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_comment, name='add_comment'),
    path('update/<int:id>/', views.update_comment, name='update_comment'),
    path('delete/<int:id>/', views.delete_comment, name='delete_comment'),
    path('detail/<int:id>/', views.comment_detail, name='comment_detail'),


]