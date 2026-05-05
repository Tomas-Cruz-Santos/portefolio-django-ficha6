from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Licenciatura, Docente, UnidadeCurricular, Tecnologia, Projeto, TFC, Competencia, Formacao, MakingOf
from .forms import LicenciaturaForm, DocenteForm, UnidadeCurricularForm, TecnologiaForm, ProjetoForm, TFCForm, CompetenciaForm, FormacaoForm, MakingOfForm


# ── DECORATOR ──
def gestor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not request.user.groups.filter(name='gestor-portfolio').exists():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── HOME ──
def home_view(request):
    context = {
        'num_projetos': Projeto.objects.count(),
        'num_ucs': UnidadeCurricular.objects.count(),
        'num_tecnologias': Tecnologia.objects.count(),
        'num_formacoes': Formacao.objects.count(),
        'projetos_recentes': Projeto.objects.select_related('uc').prefetch_related('tecnologias').order_by('-data_inicio')[:3],
    }
    return render(request, 'portfolio/home.html', context)


# ── LISTAS ──
def licenciaturas_view(request):
    return render(request, 'portfolio/licenciaturas.html', {'licenciaturas': Licenciatura.objects.prefetch_related('ucs', 'tfcs').all()})

def docentes_view(request):
    return render(request, 'portfolio/docentes.html', {'docentes': Docente.objects.prefetch_related('ucs').all()})

def ucs_view(request):
    return render(request, 'portfolio/uc.html', {'ucs': UnidadeCurricular.objects.select_related('licenciatura').prefetch_related('docentes', 'projetos').all()})

def tecnologias_view(request):
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': Tecnologia.objects.all()})

def projetos_view(request):
    return render(request, 'portfolio/projetos.html', {'projetos': Projeto.objects.select_related('uc').prefetch_related('tecnologias').all()})

def tfcs_view(request):
    return render(request, 'portfolio/tfcs.html', {'tfcs': TFC.objects.select_related('licenciatura').prefetch_related('orientador', 'tecnologias').all()})

def competencias_view(request):
    return render(request, 'portfolio/competencias.html', {'competencias': Competencia.objects.prefetch_related('tecnologias').all()})

def formacoes_view(request):
    return render(request, 'portfolio/formacoes.html', {'formacoes': Formacao.objects.prefetch_related('tecnologias').all()})

def makingof_view(request):
    doc = MakingOf.objects.filter(documento__isnull=False).first()
    return render(request, 'portfolio/makingof.html', {
        'makingofs': MakingOf.objects.all().order_by('data'),
        'makingof_doc': doc.documento if doc else None,
        'tecnologias': Tecnologia.objects.all(),
    })


# ── DETAILS ──
def licenciaturas_detail_view(request, lic_id):
    return render(request, 'portfolio/licenciaturas_detail.html', {'licenciatura': get_object_or_404(Licenciatura, id=lic_id)})

def docentes_detail_view(request, doc_id):
    return render(request, 'portfolio/docentes_detail.html', {'docente': get_object_or_404(Docente, id=doc_id)})

def uc_detail_view(request, uc_id):
    return render(request, 'portfolio/uc_detail.html', {'uc': get_object_or_404(UnidadeCurricular, id=uc_id)})

def tecnologias_detail_view(request, tec_id):
    return render(request, 'portfolio/tecnologias_detail.html', {'tecnologia': get_object_or_404(Tecnologia, id=tec_id)})

def projetos_detail_view(request, proj_id):
    return render(request, 'portfolio/projetos_detail.html', {'projeto': get_object_or_404(Projeto, id=proj_id)})

def tfcs_detail_view(request, tfc_id):
    return render(request, 'portfolio/tfcs_detail.html', {'tfc': get_object_or_404(TFC, id=tfc_id)})

def competencias_detail_view(request, comp_id):
    return render(request, 'portfolio/competencias_detail.html', {'competencia': get_object_or_404(Competencia, id=comp_id)})

def formacoes_detail_view(request, form_id):
    return render(request, 'portfolio/formacoes_detail.html', {'formacao': get_object_or_404(Formacao, id=form_id)})

def makingof_detail_view(request, makingof_id):
    return render(request, 'portfolio/makingof_detail.html', {'makingof': get_object_or_404(MakingOf, id=makingof_id)})

def sobre_view(request):
    return render(request, 'portfolio/sobre.html', {'tecnologias': Tecnologia.objects.all()})


# ── CRUD HELPERS ──
def _crud_create(request, form_class, template, redirect_url, success_msg):
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, success_msg)
        return redirect(redirect_url)
    return render(request, template, {'form': form, 'action': 'Criar'})

def _crud_edit(request, form_class, instance, template, redirect_url, success_msg):
    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, success_msg)
        return redirect(redirect_url)
    return render(request, template, {'form': form, 'action': 'Editar', 'obj': instance})

def _crud_delete(request, instance, redirect_url, success_msg):
    if request.method == 'POST':
        instance.delete()
        messages.success(request, success_msg)
        return redirect(redirect_url)
    return render(request, 'portfolio/confirm_delete.html', {'obj': instance})


# ── LICENCIATURAS CRUD ──
@gestor_required
def licenciatura_create(request):
    return _crud_create(request, LicenciaturaForm, 'portfolio/crud_form.html', 'licenciaturas', 'Licenciatura criada!')

@gestor_required
def licenciatura_edit(request, lic_id):
    return _crud_edit(request, LicenciaturaForm, get_object_or_404(Licenciatura, id=lic_id), 'portfolio/crud_form.html', 'licenciaturas', 'Licenciatura atualizada!')

@gestor_required
def licenciatura_delete(request, lic_id):
    return _crud_delete(request, get_object_or_404(Licenciatura, id=lic_id), 'licenciaturas', 'Licenciatura eliminada!')


# ── DOCENTES CRUD ──
@gestor_required
def docente_create(request):
    return _crud_create(request, DocenteForm, 'portfolio/crud_form.html', 'docentes', 'Docente criado!')

@gestor_required
def docente_edit(request, doc_id):
    return _crud_edit(request, DocenteForm, get_object_or_404(Docente, id=doc_id), 'portfolio/crud_form.html', 'docentes', 'Docente atualizado!')

@gestor_required
def docente_delete(request, doc_id):
    return _crud_delete(request, get_object_or_404(Docente, id=doc_id), 'docentes', 'Docente eliminado!')


# ── UCS CRUD ──
@gestor_required
def uc_create(request):
    return _crud_create(request, UnidadeCurricularForm, 'portfolio/crud_form.html', 'ucs', 'UC criada!')

@gestor_required
def uc_edit(request, uc_id):
    return _crud_edit(request, UnidadeCurricularForm, get_object_or_404(UnidadeCurricular, id=uc_id), 'portfolio/crud_form.html', 'ucs', 'UC atualizada!')

@gestor_required
def uc_delete(request, uc_id):
    return _crud_delete(request, get_object_or_404(UnidadeCurricular, id=uc_id), 'ucs', 'UC eliminada!')


# ── TECNOLOGIAS CRUD ──
@gestor_required
def tecnologia_create(request):
    return _crud_create(request, TecnologiaForm, 'portfolio/crud_form.html', 'tecnologias', 'Tecnologia criada!')

@gestor_required
def tecnologia_edit(request, tec_id):
    return _crud_edit(request, TecnologiaForm, get_object_or_404(Tecnologia, id=tec_id), 'portfolio/crud_form.html', 'tecnologias', 'Tecnologia atualizada!')

@gestor_required
def tecnologia_delete(request, tec_id):
    return _crud_delete(request, get_object_or_404(Tecnologia, id=tec_id), 'tecnologias', 'Tecnologia eliminada!')


# ── PROJETOS CRUD ──
@gestor_required
def projeto_create(request):
    return _crud_create(request, ProjetoForm, 'portfolio/crud_form.html', 'projetos', 'Projeto criado!')

@gestor_required
def projeto_edit(request, proj_id):
    return _crud_edit(request, ProjetoForm, get_object_or_404(Projeto, id=proj_id), 'portfolio/crud_form.html', 'projetos', 'Projeto atualizado!')

@gestor_required
def projeto_delete(request, proj_id):
    return _crud_delete(request, get_object_or_404(Projeto, id=proj_id), 'projetos', 'Projeto eliminado!')


# ── TFCS CRUD ──
@gestor_required
def tfc_create(request):
    return _crud_create(request, TFCForm, 'portfolio/crud_form.html', 'tfcs', 'TFC criado!')

@gestor_required
def tfc_edit(request, tfc_id):
    return _crud_edit(request, TFCForm, get_object_or_404(TFC, id=tfc_id), 'portfolio/crud_form.html', 'tfcs', 'TFC atualizado!')

@gestor_required
def tfc_delete(request, tfc_id):
    return _crud_delete(request, get_object_or_404(TFC, id=tfc_id), 'tfcs', 'TFC eliminado!')


# ── COMPETENCIAS CRUD ──
@gestor_required
def competencia_create(request):
    return _crud_create(request, CompetenciaForm, 'portfolio/crud_form.html', 'competencias', 'Competência criada!')

@gestor_required
def competencia_edit(request, comp_id):
    return _crud_edit(request, CompetenciaForm, get_object_or_404(Competencia, id=comp_id), 'portfolio/crud_form.html', 'competencias', 'Competência atualizada!')

@gestor_required
def competencia_delete(request, comp_id):
    return _crud_delete(request, get_object_or_404(Competencia, id=comp_id), 'competencias', 'Competência eliminada!')


# ── FORMACOES CRUD ──
@gestor_required
def formacao_create(request):
    return _crud_create(request, FormacaoForm, 'portfolio/crud_form.html', 'formacoes', 'Formação criada!')

@gestor_required
def formacao_edit(request, form_id):
    return _crud_edit(request, FormacaoForm, get_object_or_404(Formacao, id=form_id), 'portfolio/crud_form.html', 'formacoes', 'Formação atualizada!')

@gestor_required
def formacao_delete(request, form_id):
    return _crud_delete(request, get_object_or_404(Formacao, id=form_id), 'formacoes', 'Formação eliminada!')


# ── MAKINGOF CRUD ──
@gestor_required
def makingof_create(request):
    return _crud_create(request, MakingOfForm, 'portfolio/crud_form.html', 'makingof', 'Registo criado!')

@gestor_required
def makingof_edit(request, makingof_id):
    return _crud_edit(request, MakingOfForm, get_object_or_404(MakingOf, id=makingof_id), 'portfolio/crud_form.html', 'makingof', 'Registo atualizado!')

@gestor_required
def makingof_delete(request, makingof_id):
    return _crud_delete(request, get_object_or_404(MakingOf, id=makingof_id), 'makingof', 'Registo eliminado!')