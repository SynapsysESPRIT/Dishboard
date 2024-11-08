# User/forms.py
from django import forms
from .models import User, Client, Professional, Provider, Admin
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'gender', 'address', 'phone']

class ClientForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'age', 'gender', 'address', 'phone', 'weight', 'height', 'bmi']

class ProfessionalForm(UserForm):
    class Meta(UserForm.Meta):
        model = Professional
        fields = UserForm.Meta.fields + ['years_of_experience', 'diploma', 'cin', 'matricule']

class ProviderForm(UserForm):
    class Meta(UserForm.Meta):
        model = Provider
        fields = UserForm.Meta.fields + ['company_name', 'tax_code']

class AdminForm(UserForm):
    class Meta(UserForm.Meta):
        model = Admin
        fields = UserForm.Meta.fields
