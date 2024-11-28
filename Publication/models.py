


from django.db import models

from django.core.validators import MinLengthValidator

from Recette.models import Recette

from django.utils.crypto import get_random_string

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import urllib.parse



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
    
    share_count = models.IntegerField(default=0)
    facebook_shares = models.IntegerField(default=0)
    twitter_shares = models.IntegerField(default=0)
    linkedin_shares = models.IntegerField(default=0)
    whatsapp_shares = models.IntegerField(default=0)

    def generate_share_url(self, platform):
        base_url = f"{settings.SITE_URL}/Publication/{self.id}/"
        title = urllib.parse.quote(self.titre)
        
        urls = {
            'facebook': f"https://www.facebook.com/sharer/sharer.php?u={base_url}",
            'twitter': f"https://twitter.com/intent/tweet?url={base_url}&text={title}",
            'linkedin': f"https://www.linkedin.com/shareArticle?mini=true&url={base_url}&title={title}",
            'whatsapp': f"https://api.whatsapp.com/send?text={title}%20{base_url}"
        }
        return urls.get(platform, '')



class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.confirmation_token:
            self.confirmation_token = get_random_string(64)
        super().save(*args, **kwargs)

@receiver(post_save, sender=Publication)
def send_publication_notification(sender, instance, created, **kwargs):
    if created:
        subscribers = NewsletterSubscriber.objects.filter(is_confirmed=True)
        
        # Get publication details safely
        title = getattr(instance, 'titre', 'New Publication')
        description = getattr(instance, 'description', '')
        
        for subscriber in subscribers:
            html_message = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;">
                            <h1 style="margin: 0;">New Publication Alert! 🎉</h1>
                        </div>
                        
                        <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <h2 style="color: #333; margin-bottom: 15px;">{title}</h2>
                            
                            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                                <p style="color: #666; margin: 0;">{description[:200]}...</p>
                            </div>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{settings.SITE_URL}/Publication/{instance.id}/" 
                                   style="background-color: #4CAF50; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                                    Read More
                                </a>
                            </div>
                        </div>
                    </body>
                </html>
            """
            
            send_mail(
                subject=f'New Publication: {title}',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                html_message=html_message,
                fail_silently=False
            )

class Rating(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    like = models.BooleanField(default=False)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['publication', 'user']

    

