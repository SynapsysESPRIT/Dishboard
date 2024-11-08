from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Recette
from .forms import RecetteeModelForm
from django.shortcuts import render
class RecetteCreateView(CreateView):
    model = Recette
    form_class = RecetteeModelForm
    template_name = 'Recette/ajouter.html'  # Assurez-vous de créer ce template
    #success_url = reverse_lazy('recette_list')  # Redirigez vers une vue de liste après la création

from django.shortcuts import render
from .models import Recette

def liste_recettes(request):
    # Récupérer toutes les recettes par défaut
    recettes = Recette.objects.all()

    # Filtrer par titre si le paramètre est présent
    title_query = request.GET.get('title')
    if title_query:
        recettes = recettes.filter(titre__icontains=title_query)

    # Filtrer par niveau de difficulté si le paramètre est présent
    difficulty = request.GET.get('difficulty')
    if difficulty:
        recettes = recettes.filter(difficulty_level=difficulty)

    # Filtrer par type de cuisine si le paramètre est présent
    cuisine = request.GET.get('cuisine')
    if cuisine:
        recettes = recettes.filter(cuisine__icontains=cuisine)

    # Filtrer par nombre de portions si le paramètre est présent
    servings = request.GET.get('servings')
    if servings:
        try:
            servings = int(servings)
            recettes = recettes.filter(servings=servings)
        except ValueError:
            pass  # Ignorer le filtre si la conversion échoue

    # Filtrer par temps de cuisson minimum et maximum si les paramètres sont présents
    min_cook_time = request.GET.get('min_cook_time')
    max_cook_time = request.GET.get('max_cook_time')
    if min_cook_time:
        try:
            min_cook_time = int(min_cook_time)
            recettes = recettes.filter(cook_time__gte=min_cook_time)
        except ValueError:
            pass
    if max_cook_time:
        try:
            max_cook_time = int(max_cook_time)
            recettes = recettes.filter(cook_time__lte=max_cook_time)
        except ValueError:
            pass

    # Renvoyer les recettes filtrées au template
    return render(request, 'recette/list.html', {'recettes': recettes})
