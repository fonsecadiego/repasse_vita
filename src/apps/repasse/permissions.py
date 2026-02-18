from django.core.exceptions import PermissionDenied


def assert_medico(user):
    if not user.is_authenticated:
        raise PermissionDenied("Autenticação obrigatória")
    if not hasattr(user, "medico"):
        raise PermissionDenied("Usuário não vinculado a médico")


def assert_gestor(user):
    if not user.is_authenticated:
        raise PermissionDenied("Autenticação obrigatória")
    if not (user.is_staff or user.groups.filter(name="gestor").exists()):
        raise PermissionDenied("Permissão de gestor obrigatória")
