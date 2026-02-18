from django.db.models import Model

from apps.repasse.models import (
    ConvenioCatalog,
    EscalaCatalog,
    LeituraCatalog,
    ProcedimentoCatalog,
    TipoProcedCatalog,
    UnidadeCatalog,
)

CATALOG_MODELS = {
    "unidades": UnidadeCatalog,
    "convenios": ConvenioCatalog,
    "escalas": EscalaCatalog,
    "tipos_proced": TipoProcedCatalog,
    "procedimentos": ProcedimentoCatalog,
    "leituras": LeituraCatalog,
}


def get_catalog_model(catalog_key: str) -> type[Model]:
    return CATALOG_MODELS[catalog_key]


def list_catalog_items(model_class: type[Model], *, search: str = "", only_active: bool = False):
    queryset = model_class.objects.all().order_by("nome")
    if only_active:
        queryset = queryset.filter(ativo=True)
    if search:
        queryset = queryset.filter(nome__icontains=search.strip())
    return queryset


def get_catalog_item_by_id(model_class: type[Model], item_id: int):
    return model_class.objects.get(id=item_id)


def get_catalog_item_by_name_ci(model_class: type[Model], nome: str):
    return model_class.objects.filter(nome__iexact=nome.strip()).first()


def get_regra_form_choices(
    *,
    unidade_atual: str = "",
    convenio_atual: str = "",
    escala_atual: str = "",
    tipo_proced_atual: str = "",
    procedimento_atual: str = "",
    leitura_atual: str = "",
) -> dict:
    return {
        "unidade": _choices_with_current(UnidadeCatalog, unidade_atual),
        "convenio": _choices_with_current(ConvenioCatalog, convenio_atual),
        "escala": _choices_with_current(EscalaCatalog, escala_atual),
        "tipo_proced": _choices_with_current(TipoProcedCatalog, tipo_proced_atual),
        "procedimento": _choices_with_current(ProcedimentoCatalog, procedimento_atual),
        "leitura": _choices_with_current(LeituraCatalog, leitura_atual),
    }


def _choices_with_current(model_class: type[Model], current_value: str):
    options = list(model_class.objects.filter(ativo=True).values_list("nome", flat=True).order_by("nome"))
    current = (current_value or "").strip()
    if current and current != "*" and current not in options:
        options = [current, *options]
    return [("*", "* (qualquer)")] + [(opt, opt) for opt in options]


def list_unidades_catalog(only_active: bool = True):
    return list_catalog_items(UnidadeCatalog, only_active=only_active)


def list_convenios_catalog(only_active: bool = True):
    return list_catalog_items(ConvenioCatalog, only_active=only_active)


def list_escalas_catalog(only_active: bool = True):
    return list_catalog_items(EscalaCatalog, only_active=only_active)


def list_tipos_proced_catalog(only_active: bool = True):
    return list_catalog_items(TipoProcedCatalog, only_active=only_active)


def list_procedimentos_catalog(only_active: bool = True):
    return list_catalog_items(ProcedimentoCatalog, only_active=only_active)


def list_leituras_catalog(only_active: bool = True):
    return list_catalog_items(LeituraCatalog, only_active=only_active)
