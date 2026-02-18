from django.db import models


class ProducaoLaudo(models.Model):
    unidade = models.CharField(max_length=255)
    leitura = models.CharField(max_length=32)
    dt_laudo = models.DateField(db_index=True)
    dt_exame = models.DateField(null=True, blank=True)
    nr_prescricao = models.BigIntegerField()
    nome_paciente = models.CharField(max_length=255)
    ds_proced = models.CharField(max_length=255, db_index=True)
    ds_tipo_proced = models.CharField(max_length=255, db_index=True)
    escala = models.CharField(max_length=255, db_index=True)
    convenio = models.CharField(max_length=255, db_index=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    valor_exame = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medico = models.ForeignKey("repasse.Medico", on_delete=models.PROTECT, related_name="producoes", db_index=True)
    hash_idempotencia = models.CharField(max_length=64, unique=True)
    repasse_calculado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    regra_aplicada = models.ForeignKey(
        "repasse.RegraRepasse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="producoes_apuradas",
    )
    vigencia_aplicada = models.ForeignKey(
        "repasse.RegraRepasseVigencia",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="producoes_apuradas",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "repasse_producao_laudo"
        indexes = [
            models.Index(fields=["dt_laudo"]),
            models.Index(fields=["medico"]),
            models.Index(fields=["convenio"]),
            models.Index(fields=["ds_tipo_proced"]),
            models.Index(fields=["ds_proced"]),
            models.Index(fields=["escala"]),
            models.Index(fields=["leitura"]),
        ]

    def __str__(self) -> str:
        return f"Laudo {self.nr_prescricao} - {self.medico.crm}"
