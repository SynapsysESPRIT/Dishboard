from django import forms
from .models import Article

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'piece_jointe']  # Spécifiez les champs que vous souhaitez inclure
        exclude = ()  # Aucun champ n'est exclu, mais vous pouvez l'utiliser si nécessaire
    
    # Champ 'titre' pour le titre de l'article
    titre = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={'style': 'width:100%;'})
    )
    
    # Champ 'contenu' pour le contenu de l'article
    contenu = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'style': 'width:100%; height:200px;'})
    )

    # Champ 'piece_jointe' pour la pièce jointe (facultatif)
    piece_jointe = forms.FileField(
        label="Attach File",
        required=False  # La pièce jointe est optionnelle
    )
