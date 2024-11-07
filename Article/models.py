from django.db import models

from django.db import models
from django.core.validators import FileExtensionValidator

class Article(models.Model):
    titre = models.CharField(max_length=50)
    contenu = models.TextField()
    piece_jointe = models.FileField(
        upload_to="articles/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg'],
                message="Only PDF and JPG files are allowed"
            )
        ]
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.titre
