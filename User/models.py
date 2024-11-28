from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator
from django.utils.crypto import get_random_string
import uuid

# Base User model
class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)  # Verification code field
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')],
        null=True,
        blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
    )
    last_name = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def generate_verification_token(self):
        self.email_verification_token = get_random_string(64)

    def generate_verification_code(self):
        self.verification_code = get_random_string(length=6, allowed_chars='0123456789')

# Client model inheriting from User
class Client(User):
    weight = models.FloatField(
        null=True,
        blank=True,
         #validators=[MinValueValidator(0), MaxValueValidator(300)]
    )  # poids
    height = models.FloatField(
        null=True,
        blank=True,
        # validators=[MinValueValidator(0), MaxValueValidator(300)]
    )  # taille
    bmi = models.FloatField(
        null=True,
        blank=True,
         #validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # BMI

    def calculate_bmi(self):
        if self.height and self.weight:
            self.bmi = self.weight / ((self.height / 100) ** 2)
            self.save()

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

# Professional model inheriting from User
class Professional(User):
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    diploma = models.CharField(max_length=255, null=True, blank=True)
    cin = models.CharField(max_length=20, unique=True)
    matricule = models.CharField(max_length=20, unique=True)
    is_approved = models.BooleanField(default=False)  # Approval field

    class Meta:
        verbose_name = 'Professional'
        verbose_name_plural = 'Professionals'

class Provider(User):
    company_name = models.CharField(max_length=255)
    tax_code = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)  # Approval field
    

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'

# Admin model inheriting from User
class Admin(User):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

from django.shortcuts import redirect

class RequireVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_verified:
            return redirect('verify_email_code')
        return self.get_response(request)
