from dataclasses import asdict

from apps.repasse.dto import DashboardFiltrosDTO
from apps.repasse.selectors.dashboard_selector import get_dashboard_options
from apps.repasse.services.apuracao_service import calcular_mes


def apurar_dashboard(*, filtros_dto: DashboardFiltrosDTO, medico_id: int | None = None):
    return calcular_mes(
        ano=filtros_dto.ano,
        mes=filtros_dto.mes,
        medico_id=medico_id,
        **filtros_dto.to_apuracao_filtros(),
    )


def get_dashboard_payload(*, filtros_dto: DashboardFiltrosDTO, medico_id: int | None = None) -> dict:
    resultado = apurar_dashboard(filtros_dto=filtros_dto, medico_id=medico_id)
    return {
        "ano": resultado.ano,
        "mes": resultado.mes,
        "totais_por_medico": resultado.totais_por_medico,
        "breakdown": resultado.breakdown,
        "filtros": asdict(filtros_dto),
    }


def get_dashboard_filter_options(*, filtros_dto: DashboardFiltrosDTO, medico_id: int | None = None) -> dict:
    return get_dashboard_options(
        ano=filtros_dto.ano,
        mes=filtros_dto.mes,
        medico_id=medico_id,
    )
