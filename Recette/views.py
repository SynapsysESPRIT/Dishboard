from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .models import Recette
from .forms import RecetteeModelForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin


class RecetteCreateView(LoginRequiredMixin, CreateView):
    model = Recette
    form_class = RecetteeModelForm
    template_name = 'Recette/ajouter.html'
    success_url = reverse_lazy('liste_recettes')
    



@login_required
def recette_detail(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    return render(request, 'recette/recette_detail.html', {'recette': recette})

class UpdateConference(UpdateView):
    model=Recette
    template_name="Recette/ajouter.html"
    form_class=RecetteeModelForm
    success_url=reverse_lazy('liste_recettes')
    
class DeleteRecette(DeleteView):
    
    model=Recette
    template_name="Recette/delete.html"
    success_url=reverse_lazy('liste_recettes')

@login_required
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

    paginator = Paginator(recettes, 6)  # 3 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'recettes': page_obj,  # Only pass the paginated recipes
        'page_obj': page_obj
    }

    # Return the recipes filtered to the template
    return render(request, 'recette/list.html', context)

    # Renvoyer les recettes filtrées au template
   
