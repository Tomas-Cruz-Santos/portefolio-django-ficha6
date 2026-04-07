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
    list_filter = ("ano_inicio",)


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ("nome", "area_especializacao", "linkedin")
    search_fields = ("nome", "area_especializacao")


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ("nome", "ano_curricular", "semestre", "licenciatura")
    search_fields = ("nome",)
    list_filter = ("ano_curricular", "semestre", "licenciatura")
    filter_horizontal = ("docentes",)


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "categoria")
    search_fields = ("nome",)
    list_filter = ("tipo", "categoria")


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("nome", "uc", "data_inicio", "data_fim", "link_github")
    search_fields = ("nome", "descricao")
    list_filter = ("uc",)
    filter_horizontal = ("tecnologias",)


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "ano", "classificacao")
    search_fields = ("titulo", "autor")
    list_filter = ("ano",)


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "nivel")
    search_fields = ("nome", "descricao")
    list_filter = ("tipo", "nivel")
    filter_horizontal = ("tecnologias",)


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "instituicao", "data_inicio", "data_fim")
    search_fields = ("nome", "instituicao")
    filter_horizontal = ("tecnologias",)


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ("entidade", "data")
    search_fields = ("descricao", "erros", "correcoes")
    list_filter = ("data",)