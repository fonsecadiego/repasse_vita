from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from apps.repasse.dto import DashboardFiltrosDTO
from apps.repasse.permissions import assert_medico
from apps.repasse.services.dashboard_service import get_dashboard_filter_options, get_dashboard_payload


class DashboardMedicoView(LoginRequiredMixin, View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest):
        assert_medico(request.user)

        try:
            filtros = DashboardFiltrosDTO.from_querydict(request.GET)
        except (TypeError, ValueError):
            return JsonResponse({"detail": "Parâmetros de filtro inválidos"}, status=400)

        medico_id = getattr(getattr(request.user, "medico", None), "id", None)
        if medico_id is None and (request.user.is_superuser or request.user.is_staff):
            medico_id_raw = request.GET.get("medico_id")
            medico_id = int(medico_id_raw) if medico_id_raw and medico_id_raw.isdigit() else None

        if medico_id is None:
            return JsonResponse(
                {"detail": "Usuário não vinculado a médico. Informe ?medico_id=... (apenas admin/staff)."},
                status=400,
            )

        payload = get_dashboard_payload(filtros_dto=filtros, medico_id=medico_id)

        if request.GET.get("format") == "json":
            return JsonResponse(payload)

        payload["options"] = get_dashboard_filter_options(filtros_dto=filtros, medico_id=medico_id)
        return render(request, "repasse/dashboard_medico.html", payload)
