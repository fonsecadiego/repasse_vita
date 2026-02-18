from django.db import models
from django.db.models.functions import Lower


class CatalogBase(models.Model):
    nome = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class UnidadeCatalog(CatalogBase):
    class Meta(CatalogBase.Meta):
        db_table = "repasse_catalog_unidade"
        constraints = [models.UniqueConstraint(Lower("nome"), name="repasse_catalog_unidade_nome_ci_uniq")]


class ConvenioCatalog(CatalogBase):
    class Meta(CatalogBase.Meta):
        db_table = "repasse_catalog_convenio"
        constraints = [models.UniqueConstraint(Lower("nome"), name="repasse_catalog_convenio_nome_ci_uniq")]


class EscalaCatalog(CatalogBase):
    class Meta(CatalogBase.Meta):
        db_table = "repasse_catalog_escala"
        constraints = [models.UniqueConstraint(Lower("nome"), name="repasse_catalog_escala_nome_ci_uniq")]


class TipoProcedCatalog(CatalogBase):
    class Meta(CatalogBase.Meta):
        db_table = "repasse_catalog_tipo_proced"
        constraints = [models.UniqueConstraint(Lower("nome"), name="repasse_catalog_tipo_proced_nome_ci_uniq")]


class ProcedimentoCatalog(CatalogBase):
    class Meta(CatalogBase.Meta):
        db_table = "repasse_catalog_procedimento"
        constraints = [models.UniqueConstraint(Lower("nome"), name="repasse_catalog_proced_nome_ci_uniq")]


class LeituraCatalog(CatalogBase):
    class Meta(CatalogBase.Meta):
        db_table = "repasse_catalog_leitura"
        constraints = [models.UniqueConstraint(Lower("nome"), name="repasse_catalog_leitura_nome_ci_uniq")]
