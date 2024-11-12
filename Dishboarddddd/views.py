# views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Matches 'home.html' in the templates directory
