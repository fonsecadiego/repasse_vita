from datetime import date

from apps.repasse.models import Medico, RegraRepasse, RegraRepasseVigencia


def list_medicos():
    return Medico.objects.select_related("user").order_by("nome")


def get_medico_by_id(medico_id: int) -> Medico:
    return Medico.objects.get(id=medico_id)


def list_regras():
    return RegraRepasse.objects.prefetch_related("vigencias").order_by("-prioridade", "id")


def get_regra_by_id(regra_id: int) -> RegraRepasse:
    return RegraRepasse.objects.get(id=regra_id)


def list_vigencias_by_regra(regra_id: int):
    return RegraRepasseVigencia.objects.filter(regra_id=regra_id).order_by("-vigente_de", "-id")


def get_vigencia_by_id(vigencia_id: int) -> RegraRepasseVigencia:
    return RegraRepasseVigencia.objects.select_related("regra").get(id=vigencia_id)


def has_vigencia_overlap(regra_id: int, vigente_de, vigente_ate, *, exclude_id: int | None = None) -> bool:
    queryset = RegraRepasseVigencia.objects.filter(regra_id=regra_id)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    fim = vigente_ate or date.max
    for vigencia in queryset.only("vigente_de", "vigente_ate"):
        atual_fim = vigencia.vigente_ate or date.max
        if vigente_de <= atual_fim and vigencia.vigente_de <= fim:
            return True
    return False
