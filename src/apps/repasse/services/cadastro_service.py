from django.db import transaction

from apps.repasse.models import Medico, RegraRepasse, RegraRepasseVigencia
from apps.repasse.selectors.cadastro_selector import has_vigencia_overlap


@transaction.atomic
def criar_medico(data: dict) -> Medico:
    return Medico.objects.create(**data)


@transaction.atomic
def atualizar_medico(medico: Medico, data: dict) -> Medico:
    for key, value in data.items():
        setattr(medico, key, value)
    medico.save()
    return medico


@transaction.atomic
def criar_regra(data: dict) -> RegraRepasse:
    return RegraRepasse.objects.create(**data)


@transaction.atomic
def atualizar_regra(regra: RegraRepasse, data: dict) -> RegraRepasse:
    for key, value in data.items():
        setattr(regra, key, value)
    regra.save()
    return regra


def _validar_sobreposicao(regra_id: int, vigente_de, vigente_ate, *, exclude_id: int | None = None):
    if has_vigencia_overlap(regra_id, vigente_de, vigente_ate, exclude_id=exclude_id):
        raise ValueError("Já existe uma vigência sobreposta para esta regra.")


@transaction.atomic
def criar_vigencia(data: dict) -> RegraRepasseVigencia:
    _validar_sobreposicao(data["regra"].id, data["vigente_de"], data.get("vigente_ate"))
    return RegraRepasseVigencia.objects.create(**data)


@transaction.atomic
def atualizar_vigencia(vigencia: RegraRepasseVigencia, data: dict) -> RegraRepasseVigencia:
    regra = data.get("regra", vigencia.regra)
    vigente_de = data.get("vigente_de", vigencia.vigente_de)
    vigente_ate = data.get("vigente_ate", vigencia.vigente_ate)
    _validar_sobreposicao(regra.id, vigente_de, vigente_ate, exclude_id=vigencia.id)

    for key, value in data.items():
        setattr(vigencia, key, value)
    vigencia.save()
    return vigencia
