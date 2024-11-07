


from django.db import models

from django.core.validators import MinLengthValidator

from Recette.models import Recette


class Publication(models.Model):
    # Fields
    title = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(5, "Le titre doit contenir au moins 5 caractères.")
        ]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recette=models.ForeignKey(Recette,on_delete=models.CASCADE)


    # String representation of the model
    def __str__(self):
        return self.title

    # Meta information for ordering and verbose names
    class Meta:
        ordering = ['-created_at']
        
