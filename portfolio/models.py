from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    regime = models.CharField(max_length=100)
    ano_inicio = models.IntegerField()
    ano_fim = models.IntegerField(null=True, blank=True)
    ects = models.IntegerField()
    media = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Docente(models.Model):
    nome = models.CharField(max_length=200)
    area_especializacao = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    foto = models.ImageField(upload_to="docentes/", blank=True, null=True)

    def __str__(self):
        return self.nome


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    avaliacao = models.TextField(blank=True)
    dificuldade = models.CharField(max_length=100, blank=True)
    semestre = models.IntegerField()
    ano_curricular = models.IntegerField()

    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name="ucs"
    )

    docentes = models.ManyToManyField(
        Docente,
        related_name="ucs",
        blank=True
    )

    def __str__(self):
        return self.nome


class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    link_github = models.URLField(blank=True)

    uc = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name="projetos"
    )

    tecnologias = models.ManyToManyField(
        Tecnologia,
        blank=True,
        related_name="projetos"
    )

    def __str__(self):
        return self.nome


class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.IntegerField()
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=100)

    tecnologias = models.ManyToManyField(
        Tecnologia,
        blank=True,
        related_name="competencias"
    )

    def __str__(self):
        return self.nome


class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    certificado = models.FileField(upload_to="certificados/", blank=True, null=True)
    carga_horaria = models.IntegerField(null=True, blank=True)
    instituicao = models.CharField(max_length=200)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    tecnologias = models.ManyToManyField(
        Tecnologia,
        blank=True,
        related_name="formacoes"
    )

    def __str__(self):
        return self.nome


class TFC(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200, blank=True)
    ano = models.IntegerField()
    classificacao = models.FloatField(null=True, blank=True)
    relatorio = models.URLField(blank=True)

    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name="tfcs"
    )

    def __str__(self):
        return self.titulo


class MakingOf(models.Model):
    entidade = models.CharField(max_length=100)
    data = models.DateField(auto_now_add=True)
    descricao = models.TextField()
    erros = models.TextField(blank=True)
    correcoes = models.TextField(blank=True)
    fotos = models.ImageField(upload_to="makingof/", blank=True, null=True)

    def __str__(self):
        return f"{self.entidade} - {self.data}"