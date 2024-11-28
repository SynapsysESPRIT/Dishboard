# User/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Client, Professional, Provider, Admin
from .forms import ClientForm, ProfessionalForm, ProviderForm, UserForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.crypto import get_random_string


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
        if 'send_verification_code' in request.POST:
            send_verification_code(user, request)
            return HttpResponse("Verification code sent to your email.")
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail_update', user_id=user.id)
    else:
        form = UserForm(instance=user)
    return render(request, 'User/settings.html', {'user': user, 'form': form})

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
        client = form.save(commit=False)
        client.set_password(form.cleaned_data['password1'])
        client.save()
        send_verification_email(client, request)
        return HttpResponse("Check your email to verify your account.")
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


from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site


def verify_verification_code(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        try:
            user = User.objects.get(verification_code=code)
            if user:
                user.is_verified = True
                user.verification_code = None
                user.save()
                return HttpResponse("Your email has been verified successfully!")
        except User.DoesNotExist:
            return HttpResponse("Invalid verification code.")
    return render(request, 'User/verify_code.html')

def send_verification_email(user, request):
    user.generate_verification_code()
    user.save()
    
    current_site = get_current_site(request)
    verification_link = request.build_absolute_uri(
        reverse('verify_email', args=[user.email_verification_token])
    )

    send_mail(
        'Verify Your Email Address',
        f'Hi {user.username},\n\nPlease verify your email address by clicking the link below:\n{verification_link}\n\nAlternatively, you can use the verification code: {user.verification_code}\n\nThank you!',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token, is_verified=False)
        user.is_verified = True
        user.verification_code = None  # Clear the code after verification
        user.save()
        return HttpResponse("Your email has been verified successfully!")
    except User.DoesNotExist:
        return HttpResponse("Invalid or expired verification link.")