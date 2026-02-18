from apps.repasse.models import Medico


def get_medico_by_crm(crm: str) -> Medico | None:
    return Medico.objects.filter(crm=crm).first()


def get_medico_by_user_id(user_id: int) -> Medico | None:
    return Medico.objects.filter(user_id=user_id, ativo=True).first()
