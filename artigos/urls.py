from django.urls import path
from . import views

urlpatterns = [
    path('', views.artigos_view, name='artigos'),
    path('<int:artigo_id>/', views.artigo_detail_view, name='artigo_detail'),
    path('criar/', views.artigo_create, name='artigo_create'),
    path('<int:artigo_id>/editar/', views.artigo_edit, name='artigo_edit'),
    path('<int:artigo_id>/eliminar/', views.artigo_delete, name='artigo_delete'),
]