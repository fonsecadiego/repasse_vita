from datetime import date

from django.db.models import Q

from apps.repasse.models import EscalaCategoria, LeituraTipo, RegraRepasse, RegraRepasseVigencia, SocioTipo


def _wildcard_q(campo: str, valor: str | None) -> Q:
    if valor is None:
        return Q(**{f"{campo}__isnull": True}) | Q(**{campo: "*"})
    return Q(**{campo: valor}) | Q(**{campo: "*"}) | Q(**{f"{campo}__isnull": True})


def get_regras_candidatas(
    *,
    socio_tipo: str,
    leitura: str,
    unidade: str,
    tipo_proced: str,
    procedimento: str,
    convenio: str,
    escala_categoria: str,
    tempo_empresa_meses: int | None,
):
    queryset = RegraRepasse.objects.filter(ativo=True)
    queryset = queryset.filter(Q(socio_tipo=SocioTipo.AMBOS) | Q(socio_tipo=socio_tipo))
    queryset = queryset.filter(Q(leitura=LeituraTipo.AMBAS) | Q(leitura=leitura))
    queryset = queryset.filter(Q(escala_categoria=EscalaCategoria.AMBOS) | Q(escala_categoria=escala_categoria))

    queryset = queryset.filter(_wildcard_q("unidade", unidade))
    queryset = queryset.filter(_wildcard_q("tipo_proced", tipo_proced))
    queryset = queryset.filter(_wildcard_q("procedimento", procedimento))
    queryset = queryset.filter(_wildcard_q("convenio", convenio))

    if tempo_empresa_meses is not None:
        queryset = queryset.filter(
            Q(tempo_empresa_min_meses__isnull=True)
            | Q(tempo_empresa_min_meses__lte=tempo_empresa_meses)
        )

    return queryset.order_by("-prioridade", "id")


def get_vigencia_para_data(regra_id: int, data_ref: date) -> RegraRepasseVigencia | None:
    return (
        RegraRepasseVigencia.objects.filter(regra_id=regra_id, vigente_de__lte=data_ref)
        .filter(Q(vigente_ate__isnull=True) | Q(vigente_ate__gte=data_ref))
        .order_by("-vigente_de", "-id")
        .first()
    )
