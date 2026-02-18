from django.core.exceptions import PermissionDenied


def assert_medico(user):
    if not user.is_authenticated:
        raise PermissionDenied("Autenticação obrigatória")

    # bypass operacional (admin/suporte)
    if user.is_superuser or user.is_staff:
        return

    if not hasattr(user, "medico"):
        raise PermissionDenied("Usuário não vinculado a médico")


def assert_gestor(user):
    if not user.is_authenticated:
        raise PermissionDenied("Autenticação obrigatória")

    # bypass operacional (admin/suporte)
    if user.is_superuser or user.is_staff:
        return

    if not user.groups.filter(name="gestor").exists():
        raise PermissionDenied("Permissão de gestor obrigatória")
