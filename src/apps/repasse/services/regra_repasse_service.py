from dataclasses import dataclass
from datetime import date, timedelta

from django.db import transaction

from apps.repasse.models import (
    EscalaCategoria,
    LeituraTipo,
    Medico,
    RegraRepasse,
    RegraRepasseVigencia,
    SocioTipo,
    TipoCalculo,
)
from apps.repasse.selectors.regra_repasse_selector import get_regras_candidatas, get_vigencia_para_data


@dataclass
class ContextoRegraItem:
    unidade: str
    tipo_proced: str
    procedimento: str
    convenio: str
    escala: str
    leitura: str


def _map_escala_categoria(escala: str) -> str:
    escala_normalizada = (escala or "").upper()
    return EscalaCategoria.PLANTAO if "PLANTAO" in escala_normalizada else EscalaCategoria.FORA_PLANTAO


def _map_leitura(leitura: str) -> str:
    leitura_normalizada = (leitura or "").upper()
    if leitura_normalizada.startswith("1") or "PRIME" in leitura_normalizada:
        return LeituraTipo.PRIMEIRA
    if leitura_normalizada.startswith("2") or "SEG" in leitura_normalizada:
        return LeituraTipo.SEGUNDA
    return LeituraTipo.AMBAS


def _tempo_empresa_meses(medico: Medico, data_ref: date) -> int | None:
    if not medico.dt_admissao:
        return None
    return (data_ref.year - medico.dt_admissao.year) * 12 + (data_ref.month - medico.dt_admissao.month)


def _validar_vigencia_payload(tipo_calculo: str, valor_fixo, percentual) -> None:
    if tipo_calculo == TipoCalculo.FIXO and valor_fixo is None:
        raise ValueError("Vigência FIXO exige valor_fixo")
    if tipo_calculo == TipoCalculo.PERCENTUAL and percentual is None:
        raise ValueError("Vigência PERCENTUAL exige percentual")


def _validar_sem_sobreposicao(regra_id: int, vigente_de: date, vigente_ate: date | None, exclude_id: int | None = None) -> None:
    queryset = RegraRepasseVigencia.objects.filter(regra_id=regra_id)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    for vigencia in queryset:
        fim = vigente_ate or date.max
        atual_fim = vigencia.vigente_ate or date.max
        if vigente_de <= atual_fim and vigencia.vigente_de <= fim:
            raise ValueError("Sobreposição de vigências para a mesma regra")


@transaction.atomic
def criar_vigencia(
    regra_id: int,
    vigente_de: date,
    tipo_calculo: str,
    *,
    valor_fixo=None,
    percentual=None,
    motivo: str = "",
) -> RegraRepasseVigencia:
    _validar_vigencia_payload(tipo_calculo, valor_fixo, percentual)

    vigencia_atual = (
        RegraRepasseVigencia.objects.filter(regra_id=regra_id, vigente_ate__isnull=True)
        .order_by("-vigente_de")
        .first()
    )
    if vigencia_atual and vigencia_atual.vigente_de < vigente_de:
        vigencia_atual.vigente_ate = vigente_de - timedelta(days=1)
        vigencia_atual.save(update_fields=["vigente_ate"])

    _validar_sem_sobreposicao(regra_id, vigente_de, None)
    return RegraRepasseVigencia.objects.create(
        regra_id=regra_id,
        vigente_de=vigente_de,
        tipo_calculo=tipo_calculo,
        valor_fixo=valor_fixo,
        percentual=percentual,
        motivo=motivo,
    )


def pick_regra_para_item(item, medico: Medico, contexto: ContextoRegraItem) -> RegraRepasse | None:
    socio_tipo = SocioTipo.SOCIO if medico.is_socio else SocioTipo.NAO_SOCIO
    leitura = _map_leitura(contexto.leitura)
    escala_categoria = _map_escala_categoria(contexto.escala)
    tempo_empresa_meses = _tempo_empresa_meses(medico, item.dt_laudo)

    candidatos = get_regras_candidatas(
        socio_tipo=socio_tipo,
        leitura=leitura,
        unidade=contexto.unidade,
        tipo_proced=contexto.tipo_proced,
        procedimento=contexto.procedimento,
        convenio=contexto.convenio,
        escala_categoria=escala_categoria,
        tempo_empresa_meses=tempo_empresa_meses,
    )
    return candidatos.first()


def pick_vigencia_para_data(regra: RegraRepasse, data_ref: date) -> RegraRepasseVigencia | None:
    return get_vigencia_para_data(regra.id, data_ref)


def criar_regra(**kwargs) -> RegraRepasse:
    return RegraRepasse.objects.create(**kwargs)
