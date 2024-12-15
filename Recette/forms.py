from django import forms
from .models import Recette

class RecetteeModelForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ['titre', 'description', 'cuisine', 'servings', 'cook_time', 'difficulty_level', 'image', 'inventory_summary']

