from django.core.exceptions import PermissionDenied


GESTOR_GROUP_NAME = "gestor"


def is_gestor(user) -> bool:
    if user.is_superuser or user.is_staff:
        return True
    return user.groups.filter(name=GESTOR_GROUP_NAME).exists()


def is_medico(user) -> bool:
    if user.is_superuser or user.is_staff:
        return True
    return hasattr(user, "medico")


def assert_medico(user):
    if not user.is_authenticated:
        raise PermissionDenied("Autenticação obrigatória")
    if not is_medico(user):
        raise PermissionDenied("Usuário não vinculado a médico")


def assert_gestor(user):
    if not user.is_authenticated:
        raise PermissionDenied("Autenticação obrigatória")
    if not is_gestor(user):
        raise PermissionDenied("Permissão de gestor obrigatória")
