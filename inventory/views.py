from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.conf import settings
from django.http import JsonResponse
from ultralytics import YOLO
import os
import cv2

from django.shortcuts import render, redirect
from django.contrib.auth import login
from User.models import Client
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

    # Ensure the user is a client
    if not hasattr(request.user, 'client'):
        return redirect('some-error-page')  # Redirect to an error page or show an error message

    # Get the user's inventory
    user_inventory = InventoryIngredient.objects.filter(inventory__user=request.user)

    # Get the member since date
    member_since = request.user.date_joined

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
        'selected_category': selected_category,
        'member_since': member_since
    })
    
    
    
# Map YOLO model labels to human-readable names
ingredient_mapping = {
    'ingredient_2': 'garlic',
    'ingredient_3': 'ginger',
    'ingredient_4': 'apple',
    'ingredient_5': 'honey',
    'ingredient_6': 'ingredient_6_name',  # Replace with the actual ingredient name
    'ingredient_7': 'lemon',
    'ingredient_8': 'milk',
    'ingredient_9': 'ingredient_9_name',  # Replace with the actual ingredient name
    'ingredient_10': 'ingredient_10_name',  # Replace with the actual ingredient name
    'ingredient_11': 'ingredient_11_name',  # Replace with the actual ingredient name
    'ingredient_12': 'orange',
    'ingredient_13': 'lettuce',
    'ingredient_14': 'parsley',
    'ingredient_15': 'ingredient_15_name',  # Replace with the actual ingredient name
    'ingredient_16': 'meat',
    'ingredient_17': 'potato',
    'ingredient_18': 'shrimp',
    'ingredient_19': 'rice',
    'ingredient_20': 'onions',
    'ingredient_21': 'ingredient_21_name',  # Replace with the actual ingredient name
    'ingredient_22': 'tomato',
    'ingredient_23': 'ingredient_23_name',  # Replace with the actual ingredient name
    'ingredient_24': 'carrot',
    'ingredient_25': 'chicken',
    'ingredient_26': 'pepper',
    'ingredient_27': 'ingredient_27_name',  # Replace with the actual ingredient name
    'ingredient_28': 'cucumber',
    'ingredient_29': 'egg',
    'ingredient_30': 'fish',
    'ingredient_31': 'ingredient_31_name',  # Replace with the actual ingredient name
}




# Load YOLO model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'inventory/yolo_model/best.pt')
yolo_model = YOLO(MODEL_PATH)

# Retrieve class names (ingredient labels) from the YOLO model
ingredient_labels = yolo_model.names
def detect_ingredients(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_image.name)

        # Save the image temporarily
        with open(file_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # Perform YOLO inference
        image = cv2.imread(file_path)
        results = yolo_model.predict(source=image, imgsz=640, save=False, show=False)

        # Parse YOLO results
        detections = []
        missing_ingredients = []
        for box, score, class_id in zip(results[0].boxes.xyxy, results[0].boxes.conf, results[0].boxes.cls):
            if score > 0.65:  # Confidence threshold
                # Map the YOLO class ID to a human-readable ingredient name
                ingredient_id = ingredient_labels[int(class_id)]
                ingredient_name = ingredient_mapping.get(ingredient_id, None)

                if ingredient_name:
                    detections.append({
                        'label': ingredient_name,
                        'confidence': float(score),
                        'box': [int(coord) for coord in box]
                    })

                    # Check if the ingredient exists in the database
                    try:
                        ingredient = Ingredient.objects.get(label__iexact=ingredient_name)
                        # Add ingredient to inventory
                        user = request.user
                        inventory, created = Inventory.objects.get_or_create(user=user)
                        inventory_item, created = InventoryIngredient.objects.get_or_create(
                            inventory=inventory,
                            ingredient=ingredient,
                            defaults={'quantity': 1}
                        )
                        if not created:
                            inventory_item.quantity += 1
                            inventory_item.save()
                    except Ingredient.DoesNotExist:
                        missing_ingredients.append(ingredient_name)
                else:
                    missing_ingredients.append(ingredient_id)  # Add ingredient ID if no match

        # Remove the temporary image
        os.remove(file_path)

        # Return the detections as JSON
        return JsonResponse({
            'detections': detections,
            'missing_ingredients': missing_ingredients
        })

    return render(request, 'inventory/detect_ingredients.html')
