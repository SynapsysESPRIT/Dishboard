from django.urls import path
from .views import *

urlpatterns = [
    # Pour CBV
    #path('ajouter/', RecetteCreateView.as_view(), name='ajouter_recette'),
    path('recettes/', liste_recettes, name='liste_recettes'),
    path('recette/<int:pk>/', recette_detail, name='recette_detail'),
    path('recette/delete/<int:pk>/', DeleteRecette.as_view(), name='deleteClass'),
    path('recette/update/<int:pk>/', UpdateConference.as_view(), name='updateClass'),
    path('generate-recipe/', generate_recipe, name='generate_recipe'),
    path('add/', add_recipe, name='add_recipe'),
    path('ajouter_recette', add_recipe, name='ajouter_recette'),  # Ensure no trailing slash
    path('save_generated_recipe/', save_generated_recipe, name='save_generated_recipe'),
]
