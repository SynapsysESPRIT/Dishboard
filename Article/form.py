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
        widget=forms.TextInput(attrs={'style': 'width:100%; font-weight: bold;'}),
        help_text="Titre captivant."
    )
    
    # Champ 'contenu' pour le contenu de l'article
    contenu = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'style': 'width:100%; height:200px; border: 1px solid #ccc; padding: 10px;'}),
        help_text="Résumé engageant."
    )
    
    # Champ 'piece_jointe' pour la pièce jointe (facultatif)
    piece_jointe = forms.FileField(
        label="Attach File",
        required=False,
        help_text="votre image significative."
    )
    # Champ 'piece_jointe' pour la pièce jointe (facultatif)
    piece_jointe2 = forms.FileField(
        label="Attach File",
        required=False,
        help_text="votre article en pdf."
    )
