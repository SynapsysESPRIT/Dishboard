from django.urls import path

from .views import  *

urlpatterns = [

    path('', list ,name="list"),
    path('add/', AddArticle.as_view() , name="add"),
    path('details/', detailsClass, name='detailsClass'),
    #path('article/<int:pk>/', Details.as_view(), name='detailsClass'),
    #path('article/<int:pk>/', article_details, name='detailsClass'),
    #path('update/<int:pk>/', UpdateArticle.as_view(), name='updateArticle'),
    path('update/', updateClass, name='updateArticle'),
    path('delete/<int:pk>/', DeleteArticle.as_view(), name='deleteArticle'),
    #path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('blog/', blog, name='blog'),
    ]