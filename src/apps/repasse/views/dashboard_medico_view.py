from datetime import date

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from apps.repasse.permissions import assert_medico
from apps.repasse.services.apuracao_service import calcular_mes


class DashboardMedicoView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest):
        assert_medico(request.user)

        hoje = date.today()
        ano_raw = request.GET.get("ano")
        mes_raw = request.GET.get("mes")

        try:
            ano = int(ano_raw) if ano_raw else hoje.year
            mes = int(mes_raw) if mes_raw else hoje.month
        except (TypeError, ValueError):
            return JsonResponse({"detail": "Parâmetros 'ano' e 'mes' inválidos"}, status=400)

        if not (1 <= mes <= 12):
            return JsonResponse({"detail": "Parâmetro 'mes' deve estar entre 1 e 12"}, status=400)

        # médico normal: usa o vínculo user.medico
        medico_id = getattr(getattr(request.user, "medico", None), "id", None)

        # modo admin/staff: permitir informar medico_id via querystring
        if medico_id is None and (request.user.is_superuser or request.user.is_staff):
            medico_id_raw = request.GET.get("medico_id")
            try:
                medico_id = int(medico_id_raw) if medico_id_raw else None
            except (TypeError, ValueError):
                medico_id = None

        if medico_id is None:
            return JsonResponse(
                {"detail": "Usuário não vinculado a médico. Informe ?medico_id=... (apenas admin/staff)."},
                status=400,
            )

        resultado = calcular_mes(ano=ano, mes=mes, medico_id=medico_id)

        if request.GET.get("format") == "json":
            return JsonResponse(
                {
                    "ano": resultado.ano,
                    "mes": resultado.mes,
                    "totais_por_medico": resultado.totais_por_medico,
                    "breakdown": resultado.breakdown,
                }
            )

        contexto = {
            "ano": resultado.ano,
            "mes": resultado.mes,
            "totais_por_medico": resultado.totais_por_medico,
            "breakdown": resultado.breakdown,
        }

        return render(request, "repasse/dashboard_medico.html", contexto)
