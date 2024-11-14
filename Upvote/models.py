from django.db import models

class Upvote(models.Model):
    value = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Upvote {self.id} with value {self.value}"