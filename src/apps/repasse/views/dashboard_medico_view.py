from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from apps.repasse.permissions import assert_medico
from apps.repasse.services.apuracao_service import calcular_mes


class DashboardMedicoView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest):
        assert_medico(request.user)

        ano = int(request.GET.get("ano"))
        mes = int(request.GET.get("mes"))

        resultado = calcular_mes(ano=ano, mes=mes, medico_id=request.user.medico.id)

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
