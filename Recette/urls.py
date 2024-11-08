from django.urls import path
from .views import RecetteCreateView
from .views import liste_recettes
urlpatterns = [
    # Pour CBV
    path('ajouter_recette/', RecetteCreateView.as_view(), name='ajouter_recette'),
    path('recettes/', liste_recettes, name='liste_recettes'),
    # Pour FBV
    # path('ajouter_recette/', ajouter_recette, name='ajouter_recette'),

    # Autres URL ici...
]
