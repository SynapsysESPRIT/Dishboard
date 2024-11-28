from django.db import models
from django.core.validators import FileExtensionValidator
from User.models import Professional  # Import the Professional model

class Article(models.Model):
    titre = models.CharField(max_length=50)
    contenu = models.TextField()
    piece_jointe = models.FileField(
        upload_to="articles/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg'],
                message="Only PNG and JPG files are allowed"
            )
        ]
    )
    piece_jointe_2 = models.FileField(
        upload_to="articles/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf'],
                message="Only PDF files are allowed for the second attachment"
            )
        ]
    )
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='articles', null=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.titre