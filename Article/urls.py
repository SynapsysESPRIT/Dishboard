from django.urls import path

from .views import  *

urlpatterns = [

    path('', list ,name="list"),
    path('add/', AddArticle.as_view() , name="add"),
    path('details/', detailsClass, name='detailsClass'),
    path('update/', updateClass, name='updateArticle'),
    path('delete/<int:pk>/', DeleteArticle.as_view(), name='deleteArticle'),
    path('blog/', blog, name='blog'),
    ]