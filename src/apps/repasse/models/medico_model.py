from django.conf import settings
from django.db import models


class Medico(models.Model):
    nome = models.CharField(max_length=255)
    crm = models.CharField(max_length=32, unique=True, db_index=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medico",
    )
    is_socio = models.BooleanField(default=False)
    dt_admissao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "repasse_medico"
        ordering = ["nome"]

    def __str__(self) -> str:
        return f"{self.nome} ({self.crm})"
