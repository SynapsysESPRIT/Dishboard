from django.contrib import admin
from .models import Recette

class RecetteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cuisine', 'servings', 'cook_time', 'difficulty_level', 'created_at' , 'image')
    list_filter = (
        'difficulty_level',  # Filter by difficulty level
        'cuisine',           # Filter by cuisine
        'servings',          # Filter by servings
        'cook_time',  # Range filter for cook time
    )
    search_fields = ('titre',)

admin.site.register(Recette, RecetteAdmin)

