from django import forms
from .models import Article

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'piece_jointe', 'piece_jointe_2']  # Include all fields
        exclude = ()  # No fields are excluded

    # Field 'titre' for the article title
    titre = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={'style': 'width:100%; font-weight: bold;'}),
        help_text="Captivating title."
    )

    # Field 'contenu' for the article content
    contenu = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'style': 'width:100%; height:200px; border: 1px solid #ccc; padding: 10px;'}),
        help_text="Engaging summary."
    )

    # Field 'piece_jointe' for the attachment (optional)
    piece_jointe = forms.FileField(
        label="Attach File",
        required=False,
        help_text="Your significant image (jpg)."
    )

    # Field 'piece_jointe_2' for the second attachment (optional)
    piece_jointe_2 = forms.FileField(
        label="Attach File",
        required=False,
        help_text="Your article (pdf)."
    )