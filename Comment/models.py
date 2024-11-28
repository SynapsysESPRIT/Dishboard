from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from Publication.models import Publication
from User.models import User



def validate_no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Content cannot contain numbers')

def validate_no_bad_words(value):
    banned_words = ['fuck', 'bitch', 'asshole']  # Add your list of banned words
    for word in banned_words:
        if word.lower() in value.lower():
            raise ValidationError(f'The word "{word}" is not allowed in the content')

def validate_dates(updated_at):
    if updated_at < date.today():
        raise ValidationError('Update date cannot be earlier than creation date')

class Comment(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    contenu = models.CharField(
        max_length=255,
        validators=[
            validate_no_numbers,
            validate_no_bad_words,
            RegexValidator(
                regex=r'^[a-zA-Z\s.,!?-]*$',
                message='Content can only contain letters and basic punctuation'
            )
        ]
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def clean(self):
        if self.updated_at and self.created_at:
            if self.updated_at < self.created_at:
                raise ValidationError('Update date cannot be earlier than creation date')

    def __str__(self):
        return f"{self.auteur.username}: {self.contenu}"


