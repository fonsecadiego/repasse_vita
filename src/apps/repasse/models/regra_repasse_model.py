from django.db import models


class SocioTipo(models.TextChoices):
    SOCIO = "SOCIO", "Sócio"
    NAO_SOCIO = "NAO_SOCIO", "Não sócio"
    AMBOS = "AMBOS", "Ambos"


class LeituraTipo(models.TextChoices):
    PRIMEIRA = "PRIMEIRA", "Primeira"
    SEGUNDA = "SEGUNDA", "Segunda"
    AMBAS = "AMBAS", "Ambas"


class EscalaCategoria(models.TextChoices):
    PLANTAO = "PLANTAO", "Plantão"
    FORA_PLANTAO = "FORA_PLANTAO", "Fora do plantão"
    AMBOS = "AMBOS", "Ambos"


class RegraRepasse(models.Model):
    ativo = models.BooleanField(default=True)
    socio_tipo = models.CharField(max_length=16, choices=SocioTipo.choices, default=SocioTipo.AMBOS)
    leitura = models.CharField(max_length=16, choices=LeituraTipo.choices, default=LeituraTipo.AMBAS)
    unidade = models.CharField(max_length=255, null=True, blank=True, default="*")
    tipo_proced = models.CharField(max_length=255, null=True, blank=True, default="*")
    procedimento = models.CharField(max_length=255, null=True, blank=True, default="*")
    escala_categoria = models.CharField(
        max_length=16,
        choices=EscalaCategoria.choices,
        default=EscalaCategoria.AMBOS,
    )
    convenio = models.CharField(max_length=255, default="*")
    tempo_empresa_min_meses = models.PositiveIntegerField(null=True, blank=True)
    prioridade = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "repasse_regra"
        ordering = ["-prioridade", "id"]

    def __str__(self) -> str:
        return f"Regra #{self.id} (prioridade={self.prioridade})"
