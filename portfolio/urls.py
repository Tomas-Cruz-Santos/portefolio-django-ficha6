from django.urls import path
from . import views

urlpatterns = [
    # AUTH
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # HOME
    path('', views.home_view, name='home'),

    # LISTAS
    path('licenciaturas/', views.licenciaturas_view, name='licenciaturas'),
    path('docentes/', views.docentes_view, name='docentes'),
    path('ucs/', views.ucs_view, name='ucs'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('projetos/', views.projetos_view, name='projetos'),
    path('tfcs/', views.tfcs_view, name='tfcs'),
    path('competencias/', views.competencias_view, name='competencias'),
    path('formacoes/', views.formacoes_view, name='formacoes'),
    path('makingof/', views.makingof_view, name='makingof'),

    # DETAILS
    path('licenciaturas/<int:lic_id>/', views.licenciaturas_detail_view, name='licenciaturas_detail'),
    path('docentes/<int:doc_id>/', views.docentes_detail_view, name='docentes_detail'),
    path('uc/<int:uc_id>/', views.uc_detail_view, name='uc_detail'),
    path('tecnologias/<int:tec_id>/', views.tecnologias_detail_view, name='tecnologias_detail'),
    path('projetos/<int:proj_id>/', views.projetos_detail_view, name='projetos_detail'),
    path('tfcs/<int:tfc_id>/', views.tfcs_detail_view, name='tfcs_detail'),
    path('competencias/<int:comp_id>/', views.competencias_detail_view, name='competencias_detail'),
    path('formacoes/<int:form_id>/', views.formacoes_detail_view, name='formacoes_detail'),
    path('makingof/<int:makingof_id>/', views.makingof_detail_view, name='makingof_detail'),

    # CRUD — LICENCIATURAS
    path('licenciaturas/criar/', views.licenciatura_create, name='licenciatura_create'),
    path('licenciaturas/<int:lic_id>/editar/', views.licenciatura_edit, name='licenciatura_edit'),
    path('licenciaturas/<int:lic_id>/eliminar/', views.licenciatura_delete, name='licenciatura_delete'),

    # CRUD — TECNOLOGIAS
    path('tecnologias/criar/', views.tecnologia_create, name='tecnologia_create'),
    path('tecnologias/<int:tec_id>/editar/', views.tecnologia_edit, name='tecnologia_edit'),
    path('tecnologias/<int:tec_id>/eliminar/', views.tecnologia_delete, name='tecnologia_delete'),

    # CRUD — PROJETOS
    path('projetos/criar/', views.projeto_create, name='projeto_create'),
    path('projetos/<int:proj_id>/editar/', views.projeto_edit, name='projeto_edit'),
    path('projetos/<int:proj_id>/eliminar/', views.projeto_delete, name='projeto_delete'),

    # CRUD — COMPETENCIAS
    path('competencias/criar/', views.competencia_create, name='competencia_create'),
    path('competencias/<int:comp_id>/editar/', views.competencia_edit, name='competencia_edit'),
    path('competencias/<int:comp_id>/eliminar/', views.competencia_delete, name='competencia_delete'),

    # CRUD — FORMACOES
    path('formacoes/criar/', views.formacao_create, name='formacao_create'),
    path('formacoes/<int:form_id>/editar/', views.formacao_edit, name='formacao_edit'),
    path('formacoes/<int:form_id>/eliminar/', views.formacao_delete, name='formacao_delete'),

    # CRUD — MAKINGOF
    path('makingof/criar/', views.makingof_create, name='makingof_create'),
    path('makingof/<int:makingof_id>/editar/', views.makingof_edit, name='makingof_edit'),
    path('makingof/<int:makingof_id>/eliminar/', views.makingof_delete, name='makingof_delete'),
    path('sobre/', views.sobre_view, name='sobre'),

]