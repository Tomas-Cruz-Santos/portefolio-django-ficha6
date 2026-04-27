from django.shortcuts import render, get_object_or_404
from .models import Licenciatura, Docente, UnidadeCurricular, Tecnologia, Projeto, TFC, Competencia, Formacao
from .models import MakingOf

# -------- HOME --------
def home_view(request):
    context = {
        'num_projetos': Projeto.objects.count(),
        'num_ucs': UnidadeCurricular.objects.count(),
        'num_tecnologias': Tecnologia.objects.count(),
        'num_formacoes': Formacao.objects.count(),
        'projetos_recentes': Projeto.objects.select_related('uc').prefetch_related('tecnologias').order_by('-data_inicio')[:3],
    }
    return render(request, 'portfolio/home.html', context)

def licenciaturas_view(request):
    licenciaturas = Licenciatura.objects.prefetch_related('ucs', 'tfcs').all()
    return render(request, 'portfolio/licenciaturas.html', {'licenciaturas': licenciaturas})

def docentes_view(request):
    docentes = Docente.objects.prefetch_related('ucs').all()
    return render(request, 'portfolio/docentes.html', {'docentes': docentes})

def ucs_view(request):
    ucs = UnidadeCurricular.objects.select_related('licenciatura').prefetch_related('docentes', 'projetos').all()
    return render(request, 'portfolio/uc.html', {'ucs': ucs})

def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})

def projetos_view(request):
    projetos = Projeto.objects.select_related('uc').prefetch_related('tecnologias').all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})

def tfcs_view(request):
    tfcs = TFC.objects.select_related('licenciatura').prefetch_related('orientador', 'tecnologias').all()
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})

def competencias_view(request):
    competencias = Competencia.objects.prefetch_related('tecnologias').all()
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})

def formacoes_view(request):
    formacoes = Formacao.objects.prefetch_related('tecnologias').all()
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})

def makingof_view(request):
    makingofs = MakingOf.objects.all().order_by('data')
    doc = MakingOf.objects.filter(documento__isnull=False).first()
    return render(request, 'portfolio/makingof.html', {
        'makingofs': makingofs,
        'makingof_doc': doc.documento if doc else None,
    })



# -------- LICENCIATURA --------
def licenciaturas_detail_view(request, lic_id):
    licenciatura = get_object_or_404(Licenciatura, id=lic_id)
    return render(request, 'portfolio/licenciaturas_detail.html', {'licenciatura': licenciatura})

# -------- DOCENTE --------
def docentes_detail_view(request, doc_id):
    docente = get_object_or_404(Docente, id=doc_id)
    return render(request, 'portfolio/docentes_detail.html', {'docente': docente})

# -------- UC --------
def uc_detail_view(request, uc_id):
    uc = get_object_or_404(UnidadeCurricular, id=uc_id)
    return render(request, 'portfolio/uc_detail.html', {'uc': uc})

# -------- TECNOLOGIA --------
def tecnologias_detail_view(request, tec_id):
    tecnologia = get_object_or_404(Tecnologia, id=tec_id)
    return render(request, 'portfolio/tecnologias_detail.html', {'tecnologia': tecnologia})

# -------- PROJETO --------
def projetos_detail_view(request, proj_id):
    projeto = get_object_or_404(Projeto, id=proj_id)
    return render(request, 'portfolio/projetos_detail.html', {'projeto': projeto})

# -------- TFC --------
def tfcs_detail_view(request, tfc_id):
    tfc = get_object_or_404(TFC, id=tfc_id)
    return render(request, 'portfolio/tfcs_detail.html', {'tfc': tfc})

# -------- COMPETENCIA --------
def competencias_detail_view(request, comp_id):
    competencia = get_object_or_404(Competencia, id=comp_id)
    return render(request, 'portfolio/competencias_detail.html', {'competencia': competencia})

# -------- FORMACAO --------
def formacoes_detail_view(request, form_id):
    formacao = get_object_or_404(Formacao, id=form_id)
    return render(request, 'portfolio/formacoes_detail.html', {'formacao': formacao})

# -------- MAKING OF --------
def makingof_detail_view(request, makingof_id):
    makingof = get_object_or_404(MakingOf, id=makingof_id)
    return render(request, 'portfolio/makingof_detail.html', {'makingof': makingof})