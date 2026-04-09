from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    regime = models.CharField(max_length=100, blank=True)
    ano_inicio = models.IntegerField()
    ano_fim = models.IntegerField(null=True, blank=True)
    ects = models.IntegerField(null=True, blank=True)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Licenciaturas"


class Docente(models.Model):
    nome = models.CharField(max_length=200)
    area_especializacao = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True)
    foto = models.ImageField(upload_to="docentes/", blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Docentes"
        ordering = ["nome"]


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    semestre = models.IntegerField()
    ano_curricular = models.IntegerField()
    ects = models.IntegerField(null=True, blank=True)
    cod_curso = models.IntegerField(null=True, blank=True)
    cod_uc = models.IntegerField(null=True, blank=True)

    licenciatura = models.ForeignKey(
        Licenciatura, on_delete=models.CASCADE, related_name="ucs"
    )

    docentes = models.ManyToManyField(
        Docente, blank=True, related_name="ucs"
    )

    objetivos = models.TextField(blank=True)
    programa = models.TextField(blank=True)
    metodologia = models.TextField(blank=True)
    bibliografia = models.TextField(blank=True)
    natureza = models.CharField(max_length=50, blank=True)

    def __str__(self):  
        return self.nome

    class Meta:
        verbose_name_plural = "Unidades Curriculares"
        ordering = ["ano_curricular", "semestre", "nome"]

class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to="tecnologias/", blank=True, null=True)
    url = models.URLField(blank=True)
    preferencia = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Tecnologias"


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    link_github = models.URLField(blank=True)
    descricao = models.TextField(blank=True)
    foto = models.ImageField(upload_to="projetos/", blank=True, null=True)
    video = models.URLField(blank=True)

    uc = models.ForeignKey(
        UnidadeCurricular, on_delete=models.CASCADE, related_name="projetos"
    )

    tecnologias = models.ManyToManyField(
        Tecnologia, blank=True, related_name="projetos"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Projetos"


class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.IntegerField()
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, blank=True)

    tecnologias = models.ManyToManyField(
        Tecnologia, blank=True, related_name="competencias"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Competências"


class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    certificado = models.FileField(upload_to="certificados/", blank=True, null=True)
    carga_horaria = models.IntegerField(null=True, blank=True)
    instituicao = models.CharField(max_length=200, blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    tecnologias = models.ManyToManyField(
        Tecnologia, blank=True, related_name="formacoes"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Formações"


class TFC(models.Model):
    CLASSIFICACAO_CHOICES = [
        (1, "Insuficiente"),
        (2, "Suficiente"),
        (3, "Bom"),
        (4, "Muito Bom"),
        (5, "Perfeito"),
    ]

    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200, blank=True)
    curso = models.CharField(max_length=200, blank=True)
    resumo = models.TextField(blank=True)
    rating = models.IntegerField(choices=CLASSIFICACAO_CHOICES, null=True, blank=True)
    orientador = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    palavras_chave = models.CharField(max_length=300, null=True, blank=True)
    areas = models.CharField(max_length=300, null=True, blank=True)
    imagem = models.ImageField(upload_to="tfcs/", blank=True, null=True)

    tecnologias = models.ManyToManyField(
        Tecnologia, blank=True, related_name="tfcs"
    )

    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name="tfcs"
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "TFCs"


class MakingOf(models.Model):
    ENTIDADE_CHOICES = [
        ("licenciatura", "Licenciatura"),
        ("uc", "Unidade Curricular"),
        ("docente", "Docente"),
        ("projeto", "Projeto"),
        ("tecnologia", "Tecnologia"),
        ("tfc", "TFC"),
        ("competencia", "Competência"),
        ("formacao", "Formação"),
    ]

    entidade = models.CharField(max_length=30, choices=ENTIDADE_CHOICES)
    data = models.DateField(auto_now_add=True)
    descricao = models.TextField(blank=True)
    erros = models.TextField(blank=True)
    correcoes = models.TextField(blank=True)
    fotos = models.ImageField(upload_to="makingof/", blank=True, null=True)

    def __str__(self):
        return f"[{self.get_entidade_display()}] {self.data}"

    class Meta:
        verbose_name = "Making Of"
        verbose_name_plural = "Making Of"
        ordering = ["-data"]