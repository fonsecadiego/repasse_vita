from django.http import HttpRequest, JsonResponse
from django.views import View

from apps.repasse.permissions import assert_gestor
from apps.repasse.services.apuracao_service import calcular_mes


class DashboardGestorView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest):
        assert_gestor(request.user)

        ano = int(request.GET.get("ano"))
        mes = int(request.GET.get("mes"))
        filtros = {
            "unidade": request.GET.get("unidade"),
            "ds_tipo_proced": request.GET.get("tipo_proced"),
            "ds_proced": request.GET.get("procedimento"),
            "convenio": request.GET.get("convenio"),
            "escala": request.GET.get("escala"),
            "leitura": request.GET.get("leitura"),
        }

        resultado = calcular_mes(ano=ano, mes=mes, **filtros)
        return JsonResponse(
            {
                "ano": resultado.ano,
                "mes": resultado.mes,
                "totais_por_medico": resultado.totais_por_medico,
                "breakdown": resultado.breakdown,
            }
        )
