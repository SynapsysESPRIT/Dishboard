from django.db import models
from django.contrib.auth.models import User  # Import User model for user integration

class Ingredient(models.Model):
    label = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link inventory to a user
    ingredients = models.ManyToManyField(Ingredient, through='InventoryIngredient')

    def __str__(self):
        return f"Inventory of {self.user.username}"

class InventoryIngredient(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.label} in {self.inventory}"
