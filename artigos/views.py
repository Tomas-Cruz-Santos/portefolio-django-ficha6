from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artigo, Comentario
from .forms import ArtigoForm, ComentarioForm


def artigos_view(request):
    artigos = Artigo.objects.select_related('autor').prefetch_related('likes', 'comentarios').all()
    return render(request, 'artigos/artigos.html', {'artigos': artigos})


def artigo_detail_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    comentarios = artigo.comentarios.select_related('autor').all()
    form = ComentarioForm()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'comentario_submit' in request.POST:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.artigo = artigo
                comentario.autor = request.user
                comentario.save()
                messages.success(request, 'Comentário adicionado!')
                return redirect('artigo_detail', artigo_id=artigo.id)
        elif 'like_submit' in request.POST:
            if request.user in artigo.likes.all():
                artigo.likes.remove(request.user)
            else:
                artigo.likes.add(request.user)
            return redirect('artigo_detail', artigo_id=artigo.id)

    return render(request, 'artigos/artigo_detail.html', {
        'artigo': artigo,
        'comentarios': comentarios,
        'form': form,
    })


@login_required
def artigo_create(request):
    if not request.user.groups.filter(name='autores').exists():
        messages.error(request, 'Não tem permissão para criar artigos.')
        return redirect('artigos')
    form = ArtigoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        messages.success(request, 'Artigo criado!')
        return redirect('artigo_detail', artigo_id=artigo.id)
    return render(request, 'artigos/artigo_form.html', {'form': form, 'action': 'Criar'})


@login_required
def artigo_edit(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    if artigo.autor != request.user:
        messages.error(request, 'Só pode editar os seus próprios artigos.')
        return redirect('artigo_detail', artigo_id=artigo.id)
    form = ArtigoForm(request.POST or None, request.FILES or None, instance=artigo)
    if form.is_valid():
        form.save()
        messages.success(request, 'Artigo atualizado!')
        return redirect('artigo_detail', artigo_id=artigo.id)
    return render(request, 'artigos/artigo_form.html', {'form': form, 'action': 'Editar', 'obj': artigo})


@login_required
def artigo_delete(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    if artigo.autor != request.user:
        messages.error(request, 'Só pode eliminar os seus próprios artigos.')
        return redirect('artigo_detail', artigo_id=artigo.id)
    if request.method == 'POST':
        artigo.delete()
        messages.success(request, 'Artigo eliminado!')
        return redirect('artigos')
    return render(request, 'artigos/artigo_confirm_delete.html', {'obj': artigo})