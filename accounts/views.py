import uuid
import sys
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .forms import LoginForm, RegisterForm, MagicLinkForm
from .models import MagicLinkToken


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            autores_group, _ = Group.objects.get_or_create(name='autores')
            user.groups.add(autores_group)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('artigos')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST' and 'login_submit' in request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('artigos')
            else:
                messages.error(request, 'Utilizador ou password incorretos.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'magic_link_form': MagicLinkForm(),
    })


def logout_view(request):
    logout(request)
    return redirect('login')


def magic_link_request(request):
    if request.method == 'POST':
        form = MagicLinkForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Nenhuma conta encontrada com este email.')
                return redirect('login')

            token = MagicLinkToken.objects.create(
                user=user,
                token=str(uuid.uuid4()),
            )
            link = request.build_absolute_uri(f'/accounts/magic-link/verify/{token.token}/')

            if settings.DEBUG:
                print(f'\n{"=" * 60}\nMAGIC LINK:\n{link}\n{"=" * 60}\n', flush=True, file=sys.stderr)
                messages.success(request, 'Link gerado! Copia o URL da consola do servidor.')
            else:
                from django.core.mail import EmailMessage
                EmailMessage(
                    subject='O teu link de acesso',
                    body=f'Clica aqui para entrar:\n\n{link}\n\nExpira em 15 minutos.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                ).send()
                messages.success(request, 'Link enviado! Verifica o teu email.')

    return redirect('login')


def magic_link_verify(request, token):
    try:
        magic = MagicLinkToken.objects.get(token=token)
    except MagicLinkToken.DoesNotExist:
        messages.error(request, 'Link inválido.')
        return redirect('login')

    if magic.used:
        messages.error(request, 'Este link já foi utilizado.')
        return redirect('login')

    if timezone.now() > magic.created_at + timedelta(minutes=15):
        messages.error(request, 'Link expirado.')
        return redirect('login')

    magic.used = True
    magic.save()

    user = magic.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('artigos')