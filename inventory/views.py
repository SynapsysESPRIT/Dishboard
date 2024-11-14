from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Ingredient, Inventory, InventoryIngredient

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Ingredient, Inventory, InventoryIngredient

def inventory_view(request):
    # Get all categories (if you have a model for Category, you can query it here, otherwise, this assumes a column in Ingredient)
    categories = Ingredient.objects.values('category').distinct()  # Assuming `category` is a field in Ingredient model
    
    # Get selected category from the request (default is 'All')
    selected_category = request.GET.get('category', 'All')
    
    # Filter ingredients based on the selected category (if any)
    if selected_category != 'All':
        ingredients = Ingredient.objects.filter(category=selected_category)
    else:
        ingredients = Ingredient.objects.all()

    # Ensure the user is logged in (aziz for testing purposes)
    if not request.user.is_authenticated:
        user = User.objects.get(username='aziz')
        login(request, user)  # Log in the user automatically if not authenticated

    # Get the user's inventory
    user_inventory = InventoryIngredient.objects.filter(inventory__user=request.user)

    if request.method == 'POST':
        # Handle adding selected ingredients to the inventory
        if 'selected_ingredients' in request.POST:
            selected_ids = request.POST.getlist('selected_ingredients')
            user = request.user  # The logged-in user

            # Get or create the user's inventory
            inventory, created = Inventory.objects.get_or_create(user=user)

            # Add selected ingredients to the user's inventory
            for ingredient_id in selected_ids:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                quantity = int(request.POST.get(f'quantity_{ingredient.id}', 1))  # Default to 1 if no quantity provided

                # Check if the ingredient already exists in the user's inventory
                existing_item = InventoryIngredient.objects.filter(inventory=inventory, ingredient=ingredient).first()

                if existing_item:
                    # If it exists, update the quantity
                    existing_item.quantity += quantity
                    existing_item.save()
                else:
                    # If it doesn't exist, create a new entry
                    InventoryIngredient.objects.create(
                        inventory=inventory,
                        ingredient=ingredient,
                        quantity=quantity
                    )

        # Handle removing or decreasing the quantity
        elif 'decrease_quantity' in request.POST:
            ingredient_id = request.POST.get('ingredient_id')
            quantity_change = int(request.POST.get('quantity_change', 1))

            # Get the corresponding inventory ingredient
            inventory_item = InventoryIngredient.objects.get(id=ingredient_id)

            # Decrease the quantity
            if inventory_item.quantity > quantity_change:
                inventory_item.quantity -= quantity_change
                inventory_item.save()
            else:
                # If the quantity is <= quantity_change, remove the ingredient from the inventory
                inventory_item.delete()

        return redirect('inventory-view')  # After the form submission, redirect to this view again to refresh

    # Pass the ingredients, current inventory, and categories to the template
    return render(request, 'inventory/inventory_list.html', {
        'ingredients': ingredients,
        'user_inventory': user_inventory,
        'categories': categories,
        'selected_category': selected_category
    })