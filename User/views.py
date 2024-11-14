# User/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Client, Professional, Provider, Admin
from .forms import UserForm, ClientForm, ProfessionalForm, ProviderForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse


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

# Detail views
@login_required
def user_detail_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail_update', user_id=user.id)
    else:
        form = UserForm(instance=user)
    return render(request, 'User/settings.html', {'user': user})

def add_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)  # Don't save yet
        user.set_password(form.cleaned_data['password'])  # Hash the password
        user.save()  # Now save to the database
        return redirect('list_users')
    return render(request, 'User/sign-up.html', {'form': form})

def add_client(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        client = form.save(commit=False)  # Don't save yet
        client.set_password(form.cleaned_data['password1'])  # Hash the password
        client.save()  # Now save to the database

        return redirect('list_clients')
    return render(request, 'User/sign-up.html', {'form': form})

def add_professional(request):
    form = ProfessionalForm(request.POST or None)
    if form.is_valid():
        professional = form.save(commit=False)  # Don't save yet
        professional.set_password(form.cleaned_data['password1'])  # Hash the password
        professional.save()  # Now save to the database
        return redirect('list_professionals')
    return render(request, 'User/sign-up-prof.html', {'form': form})

def add_provider(request):
    form = ProviderForm(request.POST or None)
    if form.is_valid():
        provider = form.save(commit=False)  # Don't save yet
        provider.set_password(form.cleaned_data['password1'])  # Hash the password
        provider.save()  # Now save to the database
        return redirect('list_providers')
    return render(request, 'User/sign-up-prov.html', {'form': form})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('list_users')
    return render(request, 'User/confirm_delete.html', {'user': user})



class Login(LoginView):
    template_name="user/login.html"
    
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_detail_update', args=[user_id])

@login_required
def profile_view(request, user_id):
    return render(request, 'settings.html', {'user_id': user_id})


