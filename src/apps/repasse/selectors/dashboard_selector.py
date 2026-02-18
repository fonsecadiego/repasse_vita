from apps.repasse.models import ProducaoLaudo


FILTER_FIELDS = {
    "unidade": "unidade",
    "convenio": "convenio",
    "escala": "escala",
    "leitura": "leitura",
    "tipo_proced": "ds_tipo_proced",
    "procedimento": "ds_proced",
}


def get_dashboard_options(*, ano: int | None = None, mes: int | None = None, medico_id: int | None = None) -> dict:
    queryset = ProducaoLaudo.objects.all()
    if ano and mes:
        queryset = queryset.filter(dt_laudo__year=ano, dt_laudo__month=mes)
    if medico_id:
        queryset = queryset.filter(medico_id=medico_id)

    options = {}
    for key, field in FILTER_FIELDS.items():
        values = queryset.exclude(**{f"{field}__isnull": True}).exclude(**{field: ""}).values_list(field, flat=True).distinct()
        options[key] = sorted(values)
    return options
