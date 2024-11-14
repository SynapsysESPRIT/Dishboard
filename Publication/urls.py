# urls.py
from django.urls import path , include
from . import views
#from Comment.views import add_comment
urlpatterns = [
    path('ajouter/', views.ajouter_publication, name='ajouter_publication'),
    path('list/', views.publication_liste, name='publication_liste'),
    path('<int:pk>/', views.publication_detail, name='publication_detail'),
    path('delete/<int:id>/', views.delete_publication, name='delete_publication'),
    path('update/<int:id>/', views.update_publication, name='update_publication'),

    # Ajoutez d'autres routes ici
   
   
]
