## escola/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cursos/', views.cursos_view, name="cursos"),
    path('curso/<int:id>', views.curso_view, name="curso"),
    path('professores/', views.professor_view, name="professores"),
    path('alunos/', views.alunos_view, name="alunos"),
    path('', views.cursos_view),   #  rota que abre diretamente a página dos cursos
]