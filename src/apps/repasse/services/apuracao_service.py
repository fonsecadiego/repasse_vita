from calendar import monthrange
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from django.db import transaction

from apps.repasse.models import ProducaoLaudo, TipoCalculo
from apps.repasse.selectors.apuracao_selector import get_breakdown, get_totais_por_medico_mes
from apps.repasse.selectors.producao_selector import get_producao_mes
from apps.repasse.services.regra_repasse_service import ContextoRegraItem, pick_regra_para_item, pick_vigencia_para_data


@dataclass
class ApuracaoDTO:
    ano: int
    mes: int
    totais_por_medico: list[dict]
    breakdown: list[dict]


def _periodo_mes(ano: int, mes: int) -> tuple[date, date]:
    ultimo_dia = monthrange(ano, mes)[1]
    return date(ano, mes, 1), date(ano, mes, ultimo_dia)


def _calcular_repasse(item: ProducaoLaudo, vigencia) -> Decimal:
    quantidade = item.quantidade or Decimal("1")
    if vigencia.tipo_calculo == TipoCalculo.FIXO:
        return (vigencia.valor_fixo or Decimal("0")) * quantidade
    return (item.valor_exame * (vigencia.percentual or Decimal("0"))) * quantidade


@transaction.atomic
def calcular_mes(ano: int, mes: int, medico_id: int | None = None, **filtros) -> ApuracaoDTO:
    inicio_mes, fim_mes = _periodo_mes(ano, mes)
    producoes = list(get_producao_mes(inicio_mes, fim_mes, medico_id=medico_id, filtros=filtros))

    atualizacoes = []
    for item in producoes:
        contexto = ContextoRegraItem(
            unidade=item.unidade,
            tipo_proced=item.ds_tipo_proced,
            procedimento=item.ds_proced,
            convenio=item.convenio,
            escala=item.escala,
            leitura=item.leitura,
        )
        regra = pick_regra_para_item(item, item.medico, contexto)
        if not regra:
            continue
        vigencia = pick_vigencia_para_data(regra, item.dt_laudo)
        if not vigencia:
            continue

        item.repasse_calculado = _calcular_repasse(item, vigencia)
        item.regra_aplicada = regra
        item.vigencia_aplicada = vigencia
        atualizacoes.append(item)

    if atualizacoes:
        ProducaoLaudo.objects.bulk_update(
            atualizacoes,
            fields=["repasse_calculado", "regra_aplicada", "vigencia_aplicada"],
        )

    queryset_final = get_producao_mes(inicio_mes, fim_mes, medico_id=medico_id, filtros=filtros)
    return ApuracaoDTO(
        ano=ano,
        mes=mes,
        totais_por_medico=get_totais_por_medico_mes(queryset_final),
        breakdown=get_breakdown(queryset_final),
    )
