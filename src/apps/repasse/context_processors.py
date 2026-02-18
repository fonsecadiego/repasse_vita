from apps.repasse.permissions import is_gestor


def repasse_nav(request):
    user = request.user
    dashboard_url_name = "repasse-dashboard-gestor" if user.is_authenticated and is_gestor(user) else "repasse-dashboard-medico"
    return {
        "repasse_is_gestor": user.is_authenticated and is_gestor(user),
        "repasse_dashboard_url_name": dashboard_url_name,
    }
