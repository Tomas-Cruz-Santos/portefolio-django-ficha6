from django.urls import path
from . import views

urlpatterns = [
    # LISTAS
    path('licenciaturas/', views.licenciaturas_view, name='licenciaturas'),
    path('docentes/', views.docentes_view, name='docentes'),
    path('ucs/', views.ucs_view, name='ucs'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('projetos/', views.projetos_view, name='projetos'),
    path('tfcs/', views.tfcs_view, name='tfcs'),
    path('competencias/', views.competencias_view, name='competencias'),
    path('formacoes/', views.formacoes_view, name='formacoes'),

    # DETAILS
    path('licenciaturas/<int:lic_id>/', views.licenciaturas_detail_view, name='licenciaturas_detail'),
    path('docentes/<int:doc_id>/', views.docentes_detail_view, name='docentes_detail'),
    path('uc/<int:uc_id>/', views.uc_detail_view, name='uc_detail'), # corrigido
    path('tecnologias/<int:tec_id>/', views.tecnologias_detail_view, name='tecnologias_detail'),
    path('projetos/<int:proj_id>/', views.projetos_detail_view, name='projetos_detail'),
    path('tfcs/<int:tfc_id>/', views.tfcs_detail_view, name='tfcs_detail'), # corrigido
    path('competencias/<int:comp_id>/', views.competencias_detail_view, name='competencias_detail'),
    path('formacoes/<int:form_id>/', views.formacoes_detail_view, name='formacoes_detail'),
    path('makingof/<int:makingof_id>/', views.makingof_detail_view, name='makingof_detail'),
]