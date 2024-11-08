# User/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .models import User, Client, Professional, Provider, Admin
from .forms import UserForm, ClientForm, ProfessionalForm, ProviderForm, AdminForm
from django.contrib.admin.views.decorators import staff_member_required

# List views
def list_users(request):
    users = User.objects.all()
    return render(request, 'User/list_users.html', {'users': users})

def list_clients(request):
    clients = Client.objects.all()
    return render(request, 'User/list_clients.html', {'clients': clients})

def list_professionals(request):
    professionals = Professional.objects.all()
    return render(request, 'User/list_professionals.html', {'professionals': professionals})

def list_providers(request):
    providers = Provider.objects.all()
    return render(request, 'User/list_providers.html', {'providers': providers})

def list_admins(request):
    admins = Admin.objects.all()
    return render(request, 'User/list_admins.html', {'admins': admins})

@staff_member_required  # Ensure only admin can access this
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if isinstance(user, (Professional, Provider)) and not user.is_approved:
        user.is_approved = True
        user.save()
    return redirect('list_' + ('professionals' if isinstance(user, Professional) else 'providers'))

# Detail views
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'User/user_detail.html', {'user': user})

# Create views
def add_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_users')
    return render(request, 'User/sign-up.html', {'form': form})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            login(request, client)
            return redirect('home')  # redirect to the desired page after signup
    else:
        form = ClientForm()
    return render(request, 'path/to/your/sign-up.html', {'form': form})

def add_professional(request):
    form = ProfessionalForm(request.POST or None)
    if form.is_valid():
        professional = form.save(commit=False)
        professional.is_approved = False  # Not approved initially
        professional.save()
        return redirect('list_professionals')
    return render(request, 'User/sign-up.html', {'form': form})

def add_provider(request):
    form = ProviderForm(request.POST or None)
    if form.is_valid():
        provider = form.save(commit=False)
        provider.is_approved = False  # Not approved initially
        provider.save()
        return redirect('list_providers')
    return render(request, 'User/sign-up.html', {'form': form})

def add_admin(request):
    form = AdminForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_admins')
    return render(request, 'User/sign-up.html', {'form': form})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user_id=user.id)
    else:
        form = UserForm(instance=user)
    return render(request, 'User/edit_user.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')
    return render(request, 'User/confirm_delete.html', {'user': user})
