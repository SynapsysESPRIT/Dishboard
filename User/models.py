from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator

# Base User model
class User(AbstractUser):
    age = models.PositiveIntegerField(
        null=True, 
        blank=True, 
         #validators=[MinValueValidator(0), MaxValueValidator(120)]
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
        # validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )
    email = models.EmailField(
        unique=True,
         #validators=[EmailValidator(message="Enter a valid email address.")]
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

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
    years_of_experience = models.PositiveIntegerField(
        null=True,
        blank=True,
         #validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # nb_années_exp
    diploma = models.CharField(max_length=255, null=True, blank=True)
    cin = models.CharField(
        max_length=20,
        unique=True,
         #validators=[RegexValidator(r'^\d{8,20}$', message="Enter a valid CIN number.")]
    )  # National ID
    matricule = models.CharField(
        max_length=20,
        unique=True,
        #validators=[RegexValidator(r'^\w{4,20}$', message="Enter a valid matricule.")]
    )

    class Meta:
        verbose_name = 'Professional'
        verbose_name_plural = 'Professionals'

# Provider model inheriting from User
class Provider(User):
    company_name = models.CharField(max_length=255)
    tax_code = models.CharField(
        max_length=20,
         #validators=[RegexValidator(r'^\d{8,20}$', message="Enter a valid tax code.")]
    )

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'

# Admin model inheriting from User
class Admin(User):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
