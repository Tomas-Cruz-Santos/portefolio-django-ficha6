from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import secrets
from .forms import LoginForm, RegisterForm, MagicLinkForm
from .models import MagicLinkToken


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    magic_form = MagicLinkForm()

    if request.method == 'POST' and 'login_submit' in request.POST:
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'home'))
            messages.error(request, 'Credenciais inválidas.')

    return render(request, 'accounts/login.html', {
        'form': form,
        'magic_form': magic_form,
    })


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        grupo, _ = Group.objects.get_or_create(name='autores')
        user.groups.add(grupo)
        login(request, user)
        messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}.')
        return redirect('home')

    return render(request, 'accounts/register.html', {'form': form})


def magic_link_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            MagicLinkToken.objects.create(user=user, token=token)
            magic_url = request.build_absolute_uri(f'/accounts/magic-link/{token}/')
            return render(request, 'accounts/magic_link_sent.html', {
                'magic_url': magic_url,
                'email': email,
            })
        except User.DoesNotExist:
            messages.error(request, 'Não existe nenhuma conta com esse email.')

    return redirect('login')


def magic_link_verify(request, token):
    expiry = timezone.now() - timedelta(minutes=15)
    try:
        magic_token = MagicLinkToken.objects.get(
            token=token,
            used=False,
            created_at__gte=expiry
        )
        user = magic_token.user
        magic_token.used = True
        magic_token.save()
        login(request, user)
        messages.success(request, f'Bem-vindo, {user.username}!')
        return redirect('home')
    except MagicLinkToken.DoesNotExist:
        messages.error(request, 'Link inválido ou expirado.')
        return redirect('login')