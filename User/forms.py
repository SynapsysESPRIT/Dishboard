# User/forms.py

from .models import User, Client, Professional, Provider
from django.contrib.auth.forms import UserCreationForm
from django import forms 

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'gender', 'address', 'phone']

class ClientForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'age', 'gender', 'address', 'phone', 'weight', 'height', 'bmi']

class ProfessionalForm(UserCreationForm):
    class Meta:
        model = Professional
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'age', 'gender', 'address', 'phone', 'years_of_experience', 'diploma', 'cin']

class ProviderForm(UserCreationForm):
    class Meta:
        model = Provider
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'age', 'gender', 'address', 'phone','company_name', 'tax_code']





