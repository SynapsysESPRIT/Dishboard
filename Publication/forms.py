# forms.py
from django import forms
from .models import Publication
from Recette.models import Recette
class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title']

    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le titre de la publication'})
    )
    


# forms.py

from django import forms
from .models import Recette

class PublicationFilterForm(forms.Form):
    title = forms.CharField(required=False, label="Titre de la publication", widget=forms.TextInput(attrs={'placeholder': 'Titre publication'}))
    recette_title = forms.CharField(required=False, label="Titre de la recette", widget=forms.TextInput(attrs={'placeholder': 'Titre recette'}))
    serving = forms.IntegerField(required=False, label="Nombre de portions")
    cook_time = forms.IntegerField(required=False, label="Temps de cuisson (minutes)")
    created_at = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(2020, 2025)))


