from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from User.models import Client
import os
import json
# Custom validator to limit file size and extension
def validate_image_file(image):
    # Validate file size (2 MB max)
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("L'image doit être inférieure à 2MB.")

    # Validate file extension
    valid_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Le fichier doit être au format .png, .jpg, .jpeg ou .pdf.")

class Recette(models.Model):
    # Fields
    titre = models.CharField(
        max_length=255, 
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]+$',
                message="Le titre ne doit contenir que des lettres, chiffres et espaces."
            )
        ]
    )

    description = models.TextField()
    # Vos autres champs...

    favorites = models.TextField(blank=True, default="[]")  # Stocke les IDs des utilisateurs sous forme de liste JSON

    def is_favorite(self, client):
        """Vérifie si l'utilisateur a ajouté cette recette aux favoris."""
        favorite_ids = json.loads(self.favorites)
        return client.id in favorite_ids

    def toggle_favorite(self, client):
        """Ajoute ou retire l'utilisateur des favoris."""
        favorite_ids = json.loads(self.favorites)
        if client.id in favorite_ids:
            favorite_ids.remove(client.id)
        else:
            favorite_ids.append(client.id)
        self.favorites = json.dumps(favorite_ids)
        self.save()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='recettes', null=True)
    description = models.TextField()
    inventory = models.TextField(help_text="Liste d'ingrédients")
    instructions = models.TextField()
    cook_time = models.IntegerField(
        validators=[MinValueValidator(1, "Le temps de cuisson doit être au moins 1 minute.")]
    )  # Cooking time in minutes
    servings = models.IntegerField(
        validators=[
            MinValueValidator(1, "Le nombre de portions doit être au moins 1."),
            MaxValueValidator(20, "Le nombre de portions doit être au maximum 20.")
        ]
    )  # Number of servings
    cuisine = models.CharField(max_length=100)
    difficulty_level = models.CharField(
        max_length=50,
        choices=[('Facile', 'Facile'), ('Moyen', 'Moyen'), ('Difficile', 'Difficile')],
        help_text="Niveau de difficulté: Facile, Moyen, Difficile"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='images/', blank=True, null=True, validators=[validate_image_file])
    # Methods for the model
    def enregistrer(self):
        # Custom logic for saving the recette
        self.save()

    def consulter(self):
        # Custom logic to view the recette
        return f"{self.titre} - {self.description}"

    def supprimer(self):
        # Custom logic for deleting the recette
        self.delete()

    # String representation of the model
    def __str__(self):
        return self.titre

    # Adding a method to validate cook_time within a certain range
    def clean(self):
     if self.cook_time is not None:
        if self.cook_time < 1 or self.cook_time > 480:  # max 8 hours
            raise ValidationError("Le temps de cuisson doit être entre 1 et 480 minutes.")

    # Meta information for ordering and verbose names
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Recette"
        verbose_name_plural = "Recettes"
