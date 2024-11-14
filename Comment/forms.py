from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Share your thoughts...',
                'rows': 4,
                'style': 'border-radius: 12px; padding: 15px; resize: vertical; box-shadow: 0 2px 4px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; font-size: 16px; transition: all 0.3s ease; background-color: #f8fafc;'
            })
        }
