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

from django.http import JsonResponse
from .models import Recette
from inventory.models import InventoryIngredient
import requests

@login_required
def generate_recipe(request):
    # Obtenir l'inventaire de l'utilisateur connecté
    user_inventory = InventoryIngredient.objects.filter(inventory__user=request.user)

    # Récupérer les ingrédients de l'inventaire
    ingredients = [item.ingredient.label for item in user_inventory]
    ingredients_list = ",".join(ingredients)

    # Utiliser l'API Spoonacular pour générer des recettes
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients_list,
        "number": 5,  # Récupérer plusieurs recettes pour diversifier
        "ranking": 2,  # Prioriser les ingrédients exacts
        "apiKey": "1f189ba4dc134083a582b76c970ff5a8",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            import random
            recipe = random.choice(recipes)  # Choisir une recette aléatoire
            return JsonResponse({"success": True, "recipe": recipe})
        else:
            return JsonResponse({"success": False, "message": "Aucune recette trouvée."})
    else:
        return JsonResponse({"success": False, "message": "Erreur lors de l'appel à l'API Spoonacular."})

class RecetteCreateView(LoginRequiredMixin, CreateView):
    model = Recette
    form_class = RecetteeModelForm
    template_name = 'Recette/ajouter.html'
    success_url = reverse_lazy('liste_recettes')

    def form_valid(self, form):
        form.instance.client = self.request.user.client
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'client'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


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


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Recette

@login_required
def liste_recettes(request):
    # Retrieve the logged-in client's recipes
    client = request.user.client  # Assuming `Client` is related to `User` as `request.user.client`
    client_recettes = Recette.objects.filter(client=client)

    # Recipes from other clients
    other_recettes = Recette.objects.exclude(client=client)

    # Apply filters for search
    title_query = request.GET.get('title')
    if title_query:
        client_recettes = client_recettes.filter(titre__icontains=title_query)
        other_recettes = other_recettes.filter(titre__icontains=title_query)

    difficulty = request.GET.get('difficulty')
    if difficulty:
        client_recettes = client_recettes.filter(difficulty_level=difficulty)
        other_recettes = other_recettes.filter(difficulty_level=difficulty)

    cuisine = request.GET.get('cuisine')
    if cuisine:
        client_recettes = client_recettes.filter(cuisine__icontains=cuisine)
        other_recettes = other_recettes.filter(cuisine__icontains=cuisine)

    servings = request.GET.get('servings')
    if servings:
        try:
            servings = int(servings)
            client_recettes = client_recettes.filter(servings=servings)
            other_recettes = other_recettes.filter(servings=servings)
        except ValueError:
            pass

    min_cook_time = request.GET.get('min_cook_time')
    max_cook_time = request.GET.get('max_cook_time')
    if min_cook_time:
        try:
            min_cook_time = int(min_cook_time)
            client_recettes = client_recettes.filter(cook_time__gte=min_cook_time)
            other_recettes = other_recettes.filter(cook_time__gte=min_cook_time)
        except ValueError:
            pass
    if max_cook_time:
        try:
            max_cook_time = int(max_cook_time)
            client_recettes = client_recettes.filter(cook_time__lte=max_cook_time)
            other_recettes = other_recettes.filter(cook_time__lte=max_cook_time)
        except ValueError:
            pass

    # Paginate recipes from other clients
    paginator = Paginator(other_recettes, 6)  # 6 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'client_recettes': client_recettes,  # Recipes for the logged-in client
        'other_recettes': page_obj,         # Paginated recipes from other clients
        'page_obj': page_obj,
    }

    return render(request, 'recette/list.html', context)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

