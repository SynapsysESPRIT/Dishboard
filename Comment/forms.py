from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'contenu']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control'})
        }
