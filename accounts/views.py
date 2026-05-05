from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets
from .forms import LoginForm, RegisterForm
from .models import MagicLinkToken

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and 'login_submit' in request.POST:
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'home'))
            messages.error(request, 'Credenciais inválidas.')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})

def magic_link_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            MagicLinkToken.objects.create(user=user, token=token)
            magic_url = request.build_absolute_uri(f'/accounts/magic/{token}/')
            print(f'\n🔗 MAGIC LINK: {magic_url}\n')  # aparece no terminal
            return render(request, 'accounts/magic_link_sent.html', {'magic_url': magic_url, 'email': email})
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado.')
    return redirect('login')

def magic_link_verify(request, token):
    expiry = timezone.now() - timedelta(minutes=15)
    try:
        t = MagicLinkToken.objects.get(token=token, used=False, created_at__gte=expiry)
        t.used = True
        t.save()
        user = t.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('home')
    except MagicLinkToken.DoesNotExist:
        messages.error(request, 'Link inválido ou expirado.')
        return redirect('login')