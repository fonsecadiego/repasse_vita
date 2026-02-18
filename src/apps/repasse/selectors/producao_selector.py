from datetime import date

from apps.repasse.models import ProducaoLaudo


def get_producao_mes(
    inicio_mes: date,
    fim_mes: date,
    medico_id: int | None = None,
    filtros: dict | None = None,
):
    queryset = ProducaoLaudo.objects.filter(dt_laudo__range=(inicio_mes, fim_mes)).select_related(
        "medico",
        "regra_aplicada",
        "vigencia_aplicada",
    )
    if medico_id:
        queryset = queryset.filter(medico_id=medico_id)

    filtros = filtros or {}
    for campo in ["unidade", "ds_tipo_proced", "ds_proced", "convenio", "escala", "leitura"]:
        valor = filtros.get(campo)
        if valor:
            queryset = queryset.filter(**{campo: valor})
    return queryset
