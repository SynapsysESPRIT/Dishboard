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

import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
@csrf_exempt  # Utilisé pour désactiver la vérification CSRF (utile pour les tests, à ne pas utiliser en production sans sécurisation)
@require_POST
@csrf_exempt  # Désactive la vérification CSRF (utile pour les tests)
@require_POST
def save_generated_recipe(request):
    try:
        data = json.loads(request.body)
        
        # Afficher les données reçues pour vérifier leur structure
        print("Données reçues:", data)
        
        # Récupérer l'utilisateur actuel (ici, assigner à None pour un test simplifié)
        client = request.user.client  # À ajuster selon le cas d'utilisation
        
        # Formater correctement l'inventaire
        inventory_data = data.get('inventory', [])
        inventory_summary = "\n- ".join(inventory_data) if inventory_data else ''

        # Créer une nouvelle recette
        recette = Recette.objects.create(
            titre=data.get('title', 'Recette sans titre'),
            description = data.get('description', 'Description non fournie.'),
            inventory_summary=inventory_summary,  # Formater l'inventaire
            instructions=data.get('instructions', 'Aucune instruction disponible'),
            cook_time=data.get('readyInMinutes', 30),
            servings=data.get('servings', 4), # Ajustez si vous avez des données pour le nombre de portions
            cuisine='Inconnue',  # Ajustez selon les données
            difficulty_level='Facile',  # Ajustez selon les données
            image=data.get('image', None),
            client=client
        )

        # Vérifiez que la recette a été correctement enregistrée
        print("Recette enregistrée:", recette)
        
        return JsonResponse({'success': True, 'message': 'Recette enregistrée avec succès.'})
    
    except Exception as e:
        # En cas d'erreur, afficher l'erreur dans les logs
        print("Erreur:", str(e))
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def generate_recipe(request):
    # Obtenir l'inventaire de l'utilisateur connecté
    user_inventory = InventoryIngredient.objects.filter(inventory__user=request.user)
    
    # Récupérer les ingrédients de l'inventaire de l'utilisateur
    ingredients = [item.ingredient.label for item in user_inventory]
    ingredients_list = ",".join(ingredients)

    # Faire l'appel à l'API Spoonacular pour récupérer des recettes
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients_list,
        "number": 5,  # Nombre de recettes à récupérer
        "ranking": 2,  # Prioriser les ingrédients exacts
        "apiKey": "1f189ba4dc134083a582b76c970ff5a8",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            # Choisir une recette aléatoire parmi celles renvoyées par l'API
            recipe = random.choice(recipes)  # Recette aléatoire
            recipe_id = recipe.get('id')
            details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
            details_params = {
                "apiKey": "1f189ba4dc134083a582b76c970ff5a8"
            }
            details_response = requests.get(details_url, params=details_params)
            if details_response.status_code == 200:
                recipe_details = details_response.json()
                return JsonResponse({"success": True, "recipe": recipe_details})
        else:
            return JsonResponse({"success": False, "message": "Aucune recette trouvée avec les ingrédients fournis."})
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
