from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import Comment

@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        # This signal will trigger when a new comment is created
        message = f"New comment by {instance.auteur.username} on {instance.publication.title}"
        # The message will be picked up by our notification system
