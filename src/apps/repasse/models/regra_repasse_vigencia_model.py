from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class TipoCalculo(models.TextChoices):
    FIXO = "FIXO", "Fixo"
    PERCENTUAL = "PERCENTUAL", "Percentual"


class RegraRepasseVigencia(models.Model):
    regra = models.ForeignKey(
        "repasse.RegraRepasse",
        on_delete=models.CASCADE,
        related_name="vigencias",
    )
    vigente_de = models.DateField()
    vigente_ate = models.DateField(null=True, blank=True)
    tipo_calculo = models.CharField(max_length=16, choices=TipoCalculo.choices)
    valor_fixo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    percentual = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    motivo = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "repasse_regra_vigencia"
        constraints = [
            models.CheckConstraint(
                check=Q(vigente_ate__isnull=True) | Q(vigente_ate__gte=models.F("vigente_de")),
                name="repasse_vigencia_periodo_valido",
            ),
        ]
        indexes = [models.Index(fields=["regra", "vigente_de", "vigente_ate"])]
        ordering = ["-vigente_de", "-id"]

    def clean(self) -> None:
        if self.tipo_calculo == TipoCalculo.FIXO and self.valor_fixo is None:
            raise ValidationError("Vigência FIXO exige valor_fixo")
        if self.tipo_calculo == TipoCalculo.PERCENTUAL and self.percentual is None:
            raise ValidationError("Vigência PERCENTUAL exige percentual")

    def __str__(self) -> str:
        return f"Vigência regra={self.regra_id} ({self.vigente_de} - {self.vigente_ate or '∞'})"
