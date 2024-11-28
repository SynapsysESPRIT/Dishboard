from django.urls import path
from .views import RecetteCreateView
from .views import *
urlpatterns = [
    # Pour CBV
    path('ajouter_recette/', RecetteCreateView.as_view(), name='ajouter_recette'),
    path('recettes/', liste_recettes, name='liste_recettes'),
    path('recette/<int:pk>/', recette_detail, name='recette_detail'),
    path('deleteclass/<int:pk>', DeleteRecette.as_view() , name="deleteClass"),
    path('updateclass/<int:pk>', UpdateConference.as_view() , name="updateClass"),

    path('toggle-favorite/<int:recette_id>/', toggle_favorite, name='toggle_favorite'),
    # path('ajouter_recette/', ajouter_recette, name='ajouter_recette'),


]
