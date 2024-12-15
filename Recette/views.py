from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .models import Recette
from .forms import RecetteeModelForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from inventory.models import InventoryIngredient
import requests

@login_required
def generate_recipe(request):
    # Obtenir l'inventaire de l'utilisateur connecté
    user_inventory = InventoryIngredient.objects.filter(inventory__user=request.user)
    print("User Inventory in generate_recipe:", user_inventory)  # Debug print

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

class RecetteCreateView(CreateView):
    model = Recette
    template_name = 'recette/ajouter.html'
    fields = ['titre', 'description', 'cuisine', 'servings', 'cook_time', 'difficulty_level', 'image']
    success_url = '/Recette/recettes/'

class RecetteCreateView(LoginRequiredMixin, CreateView):
    model = Recette
    form_class = RecetteeModelForm
    template_name = 'Recette/ajouter.html'
    success_url = reverse_lazy('liste_recettes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_inventory'] = InventoryIngredient.objects.filter(inventory__user=self.request.user)
        return context

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
    model = Recette
    template_name = "Recette/ajouter.html"
    form_class = RecetteeModelForm
    success_url = reverse_lazy('liste_recettes')

class DeleteRecette(DeleteView):
    model = Recette
    template_name = "Recette/delete.html"
    success_url = reverse_lazy('liste_recettes')

@login_required
def liste_recettes(request):
    # Retrieve the logged-in client's recipes
    client = request.user.client  # Assuming `Client` is related to `User` as `request.user.client`
    client_recettes = Recette.objects.filter(client=client)

    # Recipes from other clients
    other_recettes = Recette.objects.exclude(client=client)
    user_inventory = InventoryIngredient.objects.filter(inventory__user=request.user)
    print("User Inventory in liste_recettes:", user_inventory)  # Debug print

    # Apply filters for search
    title_query = request.GET.get('title')
    if title_query:
        client_recettes = client_recettes.filter(titre__icontains(title_query))
        other_recettes = other_recettes.filter(titre__icontains(title_query))

    difficulty = request.GET.get('difficulty')
    if difficulty:
        client_recettes = client_recettes.filter(difficulty_level=difficulty)
        other_recettes = client_recettes.filter(difficulty_level=difficulty)

    cuisine = request.GET.get('cuisine')
    if cuisine:
        client_recettes = client_recettes.filter(cuisine__icontains(cuisine))
        other_recettes = client_recettes.filter(cuisine__icontains(cuisine))

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
            client_recettes = client_recettes.filter(cook_time__gte(min_cook_time))
            other_recettes = other_recettes.filter(cook_time__gte(min_cook_time))
        except ValueError:
            pass
    if max_cook_time:
        try:
            max_cook_time = int(max_cook_time)
            client_recettes = client_recettes.filter(cook_time__lte(max_cook_time))
            other_recettes = client_recettes.filter(cook_time__lte(max_cook_time))
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
        'user_inventory': user_inventory,   # Add user_inventory to context
    }

    return render(request, 'recette/list.html', context)

from django.shortcuts import get_object_or_404

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecetteeModelForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.client = request.user.client  # Ensure the recipe is associated with the logged-in client
            recipe.save()
            form.save_m2m()

            # Initialize a list to store the formatted strings
            ingredients_summary = []

            # Handle selected ingredients and quantities
            selected_ingredients = request.POST.getlist('selected_ingredients')
            for ingredient_id in selected_ingredients:
                quantity_key = f'ingredient_quantity_{ingredient_id}'
                quantity = request.POST.get(quantity_key, 0)  # Default to 0 if not provided
                try:
                    quantity = float(quantity)  # Ensure the quantity is numeric
                    if quantity > 0:  # Only process positive quantities
                        ingredient = get_object_or_404(InventoryIngredient, id=ingredient_id)
                        # Add to the ingredients summary
                        ingredients_summary.append(f"{quantity} {ingredient.ingredient.label}")
                except (ValueError, InventoryIngredient.DoesNotExist):
                    # Skip invalid ingredient IDs or quantities
                    continue

            # Generate the final string
            ingredients_summary_str = "\n- ".join(ingredients_summary)
            print("Ingredients Summary:", ingredients_summary_str)  # Debug print
            
            # Save this summary string to the inventory_summary field in the recipe
            recipe.inventory_summary = ingredients_summary_str  # Ensure this field exists in the model
            recipe.save()

            return redirect('recette_detail', pk=recipe.pk)
    else:
        form = RecetteeModelForm()

    # Get the user's inventory
    user_inventory = InventoryIngredient.objects.filter(inventory__user=request.user)

    return render(request, 'Recette/ajouter.html', {
        'form': form,
        'user_inventory': user_inventory,
    })
