from django import forms
from .models import Recette

class RecetteeModelForm(forms.ModelForm):
    class Meta:
        
        model = Recette
        fields = ['titre', 'description', 'inventory', 'instructions', 'cook_time', 'servings', 'cuisine', 'difficulty_level', 'image']
        
