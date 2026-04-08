from django.contrib import admin

from .models import (
    Licenciatura, Docente, UnidadeCurricular,
    Tecnologia, Projeto, TFC,
    Competencia, Formacao, MakingOf
)


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ("nome", "regime", "ano_inicio", "ano_fim", "ects", "media")
    search_fields = ("nome", "regime")


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ("nome", "area_especializacao", "linkedin")
    search_fields = ("nome", "area_especializacao")


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ("nome", "licenciatura", "ano_curricular", "semestre", "dificuldade", "natureza")
    search_fields = ("nome",)
    list_filter = ("licenciatura", "ano_curricular", "semestre", "natureza")
    filter_horizontal = ("docentes",)
    autocomplete_fields = ("licenciatura",)


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "categoria", "url", "preferencia")
    search_fields = ("nome", "categoria", "tipo")
    list_filter = ("categoria", "tipo", "preferencia")


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("nome", "uc", "data_inicio", "data_fim", "link_github")
    search_fields = ("nome", "descricao")
    list_filter = ("uc__licenciatura",)
    filter_horizontal = ("tecnologias",)
    autocomplete_fields = ("uc",)


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "curso", "orientador", "rating")
    search_fields = ("titulo", "autor", "orientador", "palavras_chave", "areas")
    list_filter = ("rating", "licenciatura")
    filter_horizontal = ("tecnologias",)
    autocomplete_fields = ("licenciatura",)


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "nivel")
    search_fields = ("nome", "descricao")
    list_filter = ("tipo", "nivel")
    filter_horizontal = ("tecnologias",)


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "instituicao", "carga_horaria", "data_inicio", "data_fim")
    search_fields = ("nome", "instituicao")
    list_filter = ("instituicao",)


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ("entidade", "data")
    search_fields = ("descricao", "erros")
    list_filter = ("entidade", "data")