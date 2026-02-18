from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from apps.repasse.dto import DashboardFiltrosDTO
from apps.repasse.permissions import assert_gestor, assert_medico, is_gestor
from apps.repasse.services.dashboard_service import get_dashboard_filter_options, get_dashboard_payload


class DashboardGestorView(LoginRequiredMixin, View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest):
        assert_gestor(request.user)

        try:
            filtros = DashboardFiltrosDTO.from_querydict(request.GET)
        except (TypeError, ValueError):
            return JsonResponse({"detail": "Parâmetros de filtro inválidos"}, status=400)

        payload = get_dashboard_payload(filtros_dto=filtros)

        if request.GET.get("format") == "json":
            return JsonResponse(payload)

        payload["options"] = get_dashboard_filter_options(filtros_dto=filtros)
        return render(request, "repasse/dashboard_gestor.html", payload)


class DashboardOptionsView(LoginRequiredMixin, View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest):
        try:
            filtros = DashboardFiltrosDTO.from_querydict(request.GET)
        except (TypeError, ValueError):
            return JsonResponse({"detail": "Parâmetros de filtro inválidos"}, status=400)

        medico_id = None
        if not is_gestor(request.user):
            assert_medico(request.user)
            medico_id = getattr(getattr(request.user, "medico", None), "id", None)

        return JsonResponse(get_dashboard_filter_options(filtros_dto=filtros, medico_id=medico_id))
